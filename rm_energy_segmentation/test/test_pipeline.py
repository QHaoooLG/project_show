from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from rmvs.app import RecognitionConfig, run_recognition
from rmvs.train import TrainingConfig, train_model
from rmvs.utils import read_json


def make_dataset(root: Path) -> Path:
    dataset = root / "frames"
    images = dataset / "images"
    images.mkdir(parents=True)
    for idx in range(4):
        image = Image.new("RGB", (96, 72), (8, 8, 20))
        draw = ImageDraw.Draw(image)
        x = 18 + idx * 12
        draw.ellipse((x, 24, x + 20, 44), fill=(255, 45, 20))
        draw.rectangle((x + 20, 32, x + 42, 38), fill=(255, 180, 30))
        image.save(images / f"frame_{idx:03d}.jpg")
    return dataset


class PipelineTest(unittest.TestCase):
    def test_train_and_recognize_frame_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = make_dataset(root)
            train_result = train_model(
                TrainingConfig(
                    dataset_dir=dataset,
                    output_dir=root / "train",
                    epochs=1,
                    batch_size=2,
                    image_size=64,
                    base_channels=4,
                    verbose=False,
                )
            )
            self.assertTrue(Path(train_result["best_model"]).exists())
            summary = run_recognition(
                RecognitionConfig(
                    model_path=Path(train_result["best_model"]),
                    input_path=dataset,
                    output_dir=root / "video",
                    threshold=0.05,
                    min_area=5,
                    max_area_ratio=0.8,
                    no_window=True,
                    save_video=False,
                    max_frames=2,
                    resize_width=0,
                )
            )
            self.assertEqual(summary["processed_frames"], 2)
            self.assertTrue(Path(summary["frame_results"]).exists())
            data = read_json(Path(summary["output_dir"]) / "summary.json")
            self.assertEqual(data["processed_frames"], 2)


if __name__ == "__main__":
    unittest.main()
