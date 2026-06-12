from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from rmvs.paths import default_frame_dataset_dir, outputs_dir
from rmvs.train import TrainingConfig, train_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the energy mechanism instance segmentation model.")
    parser.add_argument("--dataset-dir", default=str(default_frame_dataset_dir()))
    parser.add_argument("--output-dir", default=str(outputs_dir() / "train_filtered"))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--image-size", type=int, default=128)
    parser.add_argument("--max-images", type=int, default=0)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--base-channels", type=int, default=8)
    parser.add_argument("--progress-interval", type=int, default=5)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = train_model(
        TrainingConfig(
            dataset_dir=Path(args.dataset_dir),
            output_dir=Path(args.output_dir),
            epochs=args.epochs,
            batch_size=args.batch_size,
            image_size=args.image_size,
            max_images=args.max_images,
            val_ratio=args.val_ratio,
            lr=args.lr,
            seed=args.seed,
            device=args.device,
            base_channels=args.base_channels,
            progress_interval=args.progress_interval,
            verbose=not args.quiet,
        )
    )
    print("Training complete")
    print(f"best_model={result['best_model']}")
    print(f"last_model={result['last_model']}")
    print(f"num_images={result['num_images']}")


if __name__ == "__main__":
    main()
