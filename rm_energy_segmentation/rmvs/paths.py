from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    return project_root() / "data"


def outputs_dir() -> Path:
    return project_root() / "outputs"


def default_frame_dataset_dir() -> Path:
    return data_dir() / "关灯红方小能量机关激活全过程_frame_dataset"


def default_video_path() -> Path:
    return data_dir() / "关灯红方小能量机关激活全过程.mp4"


def default_model_path() -> Path:
    return outputs_dir() / "train_filtered" / "best_model.pt"


def ensure_dir(path: str | Path) -> Path:
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def resolve_images_dir(path: str | Path) -> Path:
    root = Path(path)
    if (root / "images").is_dir():
        return root / "images"
    if root.is_dir():
        return root
    raise FileNotFoundError(f"Image dataset directory not found: {root}")


def list_images(path: str | Path) -> list[Path]:
    images_dir = resolve_images_dir(path)
    suffixes = {".jpg", ".jpeg", ".png", ".bmp"}
    return sorted(p for p in images_dir.iterdir() if p.suffix.lower() in suffixes)


def is_video_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in {".mp4", ".avi", ".mov", ".mkv", ".wmv"}
