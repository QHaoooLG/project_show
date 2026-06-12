from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset

from .paths import list_images
from .pseudo_label import PseudoMaskConfig, generate_energy_mask


@dataclass(frozen=True, slots=True)
class FrameItem:
    image_path: Path


def scan_frame_dataset(dataset_dir: str | Path, *, max_images: int = 0) -> list[FrameItem]:
    image_paths = list_images(dataset_dir)
    if max_images > 0:
        image_paths = image_paths[:max_images]
    if not image_paths:
        raise ValueError(f"No images found in dataset: {dataset_dir}")
    return [FrameItem(image_path=p) for p in image_paths]


def split_items(items: list[FrameItem], *, val_ratio: float, seed: int) -> tuple[list[FrameItem], list[FrameItem]]:
    shuffled = list(items)
    rng = random.Random(seed)
    rng.shuffle(shuffled)
    if len(shuffled) < 2 or val_ratio <= 0:
        return shuffled, shuffled[:]
    val_count = max(1, int(round(len(shuffled) * val_ratio)))
    val_count = min(val_count, len(shuffled) - 1)
    return shuffled[val_count:], shuffled[:val_count]


class EnergyFrameDataset(Dataset):
    def __init__(
        self,
        items: list[FrameItem],
        *,
        image_size: int,
        pseudo_config: PseudoMaskConfig | None = None,
        augment: bool = False,
    ) -> None:
        self.items = items
        self.image_size = image_size
        self.pseudo_config = pseudo_config or PseudoMaskConfig()
        self.augment = augment

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        item = self.items[index]
        image = Image.open(item.image_path).convert("RGB")
        image_np = np.asarray(image, dtype=np.uint8)
        mask_np = generate_energy_mask(image_np, self.pseudo_config)

        image = image.resize((self.image_size, self.image_size), Image.Resampling.BILINEAR)
        mask = Image.fromarray(mask_np * 255, mode="L").resize(
            (self.image_size, self.image_size),
            Image.Resampling.NEAREST,
        )
        image_arr = np.asarray(image, dtype=np.float32) / 255.0
        mask_arr = (np.asarray(mask, dtype=np.float32) > 127).astype(np.float32)

        if self.augment and random.random() < 0.5:
            image_arr = np.ascontiguousarray(image_arr[:, ::-1, :])
            mask_arr = np.ascontiguousarray(mask_arr[:, ::-1])

        image_tensor = torch.from_numpy(image_arr.transpose(2, 0, 1))
        mask_tensor = torch.from_numpy(mask_arr).unsqueeze(0)
        return image_tensor, mask_tensor


def dataset_manifest(items: list[FrameItem]) -> dict:
    return {
        "num_images": len(items),
        "items": [{"image": str(item.image_path)} for item in items],
    }
