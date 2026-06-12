from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import torch
from torch import nn
from torch.utils.data import DataLoader

from .dataset import EnergyFrameDataset, dataset_manifest, scan_frame_dataset, split_items
from .model import build_model
from .paths import default_frame_dataset_dir, ensure_dir
from .pseudo_label import PseudoMaskConfig
from .utils import set_seed, write_json


@dataclass(slots=True)
class TrainingConfig:
    dataset_dir: Path = default_frame_dataset_dir()
    output_dir: Path = Path("outputs/train_filtered")
    epochs: int = 3
    batch_size: int = 2
    image_size: int = 128
    max_images: int = 0
    val_ratio: float = 0.2
    lr: float = 1e-3
    seed: int = 42
    device: str = "cpu"
    base_channels: int = 8
    progress_interval: int = 5
    verbose: bool = True


def train_model(config: TrainingConfig) -> dict[str, Any]:
    started = time.perf_counter()
    set_seed(config.seed)
    output_dir = ensure_dir(config.output_dir)
    _log(config, f"[train] scanning dataset: {config.dataset_dir}")
    items = scan_frame_dataset(config.dataset_dir, max_images=config.max_images)
    train_items, val_items = split_items(items, val_ratio=config.val_ratio, seed=config.seed)
    pseudo_config = PseudoMaskConfig()
    train_ds = EnergyFrameDataset(train_items, image_size=config.image_size, pseudo_config=pseudo_config, augment=True)
    val_ds = EnergyFrameDataset(val_items, image_size=config.image_size, pseudo_config=pseudo_config, augment=False)
    train_loader = DataLoader(train_ds, batch_size=config.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=config.batch_size, shuffle=False, num_workers=0)

    device = _resolve_device(config.device)
    model = build_model(base_channels=config.base_channels).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=1e-4)
    bce_loss = nn.BCEWithLogitsLoss()
    metrics: list[dict[str, float]] = []
    best_val = float("inf")
    best_path = output_dir / "best_model.pt"
    last_path = output_dir / "last_model.pt"

    manifest = dataset_manifest(items)
    write_json(output_dir / "dataset_manifest.json", manifest)
    _log(
        config,
        f"[train] start: images={len(items)} train={len(train_ds)} val={len(val_ds)} "
        f"device={device} epochs={config.epochs} image_size={config.image_size} output={output_dir}",
    )

    for epoch in range(1, config.epochs + 1):
        epoch_started = time.perf_counter()
        train_loss = _run_epoch(model, train_loader, bce_loss, optimizer, device, config=config, epoch=epoch)
        val_loss, val_iou = _evaluate(model, val_loader, bce_loss, device, config=config, epoch=epoch)
        row = {
            "epoch": float(epoch),
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_foreground_iou": val_iou,
        }
        metrics.append(row)
        checkpoint = _checkpoint(model, config, metrics, pseudo_config)
        torch.save(checkpoint, last_path)
        improved = val_loss <= best_val
        if improved:
            best_val = val_loss
            torch.save(checkpoint, best_path)
        _log(
            config,
            f"[epoch {epoch}/{config.epochs}] done: train_loss={train_loss:.4f} "
            f"val_loss={val_loss:.4f} val_iou={val_iou:.4f} best={'yes' if improved else 'no'} "
            f"elapsed={_format_duration(time.perf_counter() - epoch_started)}",
        )

    serializable_config = asdict(config)
    serializable_config["dataset_dir"] = str(config.dataset_dir)
    serializable_config["output_dir"] = str(config.output_dir)
    serializable_config["pseudo_mask"] = asdict(pseudo_config)
    write_json(output_dir / "training_config.json", serializable_config)
    write_json(output_dir / "metrics.json", metrics)
    _log(
        config,
        f"[train] complete: best_model={best_path} last_model={last_path} "
        f"total_elapsed={_format_duration(time.perf_counter() - started)}",
    )
    return {
        "output_dir": str(output_dir),
        "best_model": str(best_path),
        "last_model": str(last_path),
        "metrics": metrics,
        "num_images": len(items),
    }


def _run_epoch(
    model: torch.nn.Module,
    loader: DataLoader,
    bce_loss: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    *,
    config: TrainingConfig,
    epoch: int,
) -> float:
    model.train()
    total = 0.0
    seen = 0
    for batch_index, (images, masks) in enumerate(loader, start=1):
        images = images.to(device)
        masks = masks.to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = bce_loss(logits, masks) + 0.45 * dice_loss(logits, masks)
        loss.backward()
        optimizer.step()
        batch = images.shape[0]
        total += float(loss.detach().cpu()) * batch
        seen += batch
        if _should_log(batch_index, len(loader), config.progress_interval):
            _log(
                config,
                f"[train][epoch {epoch}/{config.epochs}] batch={batch_index}/{len(loader)} "
                f"samples={seen}/{len(loader.dataset)} loss={float(loss.detach().cpu()):.4f} "
                f"avg_loss={total / max(1, seen):.4f}",
            )
    return total / max(1, seen)


@torch.no_grad()
def _evaluate(
    model: torch.nn.Module,
    loader: DataLoader,
    bce_loss: nn.Module,
    device: torch.device,
    *,
    config: TrainingConfig,
    epoch: int,
) -> tuple[float, float]:
    model.eval()
    total = 0.0
    seen = 0
    intersections = 0.0
    unions = 0.0
    for batch_index, (images, masks) in enumerate(loader, start=1):
        images = images.to(device)
        masks = masks.to(device)
        logits = model(images)
        loss = bce_loss(logits, masks) + 0.45 * dice_loss(logits, masks)
        probs = torch.sigmoid(logits)
        pred = probs >= 0.5
        true = masks >= 0.5
        intersections += float((pred & true).sum().cpu())
        unions += float((pred | true).sum().cpu())
        batch = images.shape[0]
        total += float(loss.detach().cpu()) * batch
        seen += batch
        if _should_log(batch_index, len(loader), config.progress_interval):
            _log(
                config,
                f"[val][epoch {epoch}/{config.epochs}] batch={batch_index}/{len(loader)} "
                f"samples={seen}/{len(loader.dataset)} loss={float(loss.detach().cpu()):.4f} "
                f"avg_loss={total / max(1, seen):.4f}",
            )
    return total / max(1, seen), intersections / max(1.0, unions)


def dice_loss(logits: torch.Tensor, target: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    probs = torch.sigmoid(logits)
    dims = (0, 2, 3)
    intersection = (probs * target).sum(dim=dims)
    denominator = probs.sum(dim=dims) + target.sum(dim=dims)
    dice = (2.0 * intersection + eps) / (denominator + eps)
    return 1.0 - dice.mean()


def _checkpoint(
    model: torch.nn.Module,
    config: TrainingConfig,
    metrics: list[dict[str, float]],
    pseudo_config: PseudoMaskConfig,
) -> dict[str, Any]:
    return {
        "model_state": model.state_dict(),
        "model_type": "TinyUNetBinary",
        "image_size": config.image_size,
        "base_channels": config.base_channels,
        "metrics": metrics,
        "pseudo_mask": asdict(pseudo_config),
        "config": {
            "epochs": config.epochs,
            "batch_size": config.batch_size,
            "image_size": config.image_size,
            "lr": config.lr,
            "device": config.device,
            "base_channels": config.base_channels,
        },
    }


def _resolve_device(name: str) -> torch.device:
    if name.startswith("cuda") and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(name)


def _log(config: TrainingConfig, message: str) -> None:
    if config.verbose:
        print(message, flush=True)


def _should_log(batch_index: int, total_batches: int, interval: int) -> bool:
    interval = max(1, interval)
    return batch_index == 1 or batch_index == total_batches or batch_index % interval == 0


def _format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, remaining = divmod(int(seconds), 60)
    return f"{minutes:02d}:{remaining:02d}"
