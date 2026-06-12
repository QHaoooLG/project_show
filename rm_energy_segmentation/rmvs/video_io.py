from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import cv2
import numpy as np

from .paths import is_video_file, list_images


@dataclass(slots=True)
class FramePacket:
    index: int
    time_sec: float
    frame_bgr: Any
    source_name: str


class FrameSource:
    def __init__(self, input_path: str | Path, *, fallback_fps: float = 4.0) -> None:
        _quiet_opencv_video_logs()
        self.input_path = Path(input_path)
        self.fallback_fps = fallback_fps
        self.fps = fallback_fps
        self.frame_count = 0
        self.width = 0
        self.height = 0
        self.kind = "directory"
        if self.input_path.is_file() and is_video_file(self.input_path):
            self.kind = "video"
            cap = cv2.VideoCapture(str(self.input_path))
            try:
                if not cap.isOpened():
                    raise ValueError(f"Cannot open video: {self.input_path}")
                self.fps = float(cap.get(cv2.CAP_PROP_FPS)) or fallback_fps
                self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            finally:
                cap.release()
        elif self.input_path.is_dir():
            self.images = list_images(self.input_path)
            if not self.images:
                raise ValueError(f"No images found in frame directory: {self.input_path}")
            self.kind = "directory"
            self.frame_count = len(self.images)
            self.fps = self._fps_from_manifest() or fallback_fps
            sample = read_image_bgr(self.images[0])
            if sample is None:
                raise ValueError(f"Cannot read first image: {self.images[0]}")
            self.height, self.width = sample.shape[:2]
        else:
            raise FileNotFoundError(f"Input path not found or unsupported: {self.input_path}")

    def __iter__(self) -> Iterator[FramePacket]:
        if self.kind == "video":
            yield from self._iter_video()
        else:
            yield from self._iter_directory()

    def _iter_video(self) -> Iterator[FramePacket]:
        _quiet_opencv_video_logs()
        cap = cv2.VideoCapture(str(self.input_path))
        try:
            index = 0
            retry_count = 0
            while True:
                ok, frame = cap.read()
                if not ok or frame is None:
                    if self.frame_count > 0 and index < self.frame_count and retry_count < 3:
                        retry_count += 1
                        cap.release()
                        cap = cv2.VideoCapture(str(self.input_path))
                        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                        ok, frame = cap.read()
                    if not ok or frame is None:
                        break
                retry_count = 0
                yield FramePacket(index=index, time_sec=index / max(self.fps, 1e-6), frame_bgr=frame, source_name=self.input_path.name)
                index += 1
        finally:
            cap.release()

    def _iter_directory(self) -> Iterator[FramePacket]:
        for index, image_path in enumerate(self.images):
            frame = read_image_bgr(image_path)
            if frame is None:
                continue
            yield FramePacket(index=index, time_sec=index / max(self.fps, 1e-6), frame_bgr=frame, source_name=image_path.name)

    def _fps_from_manifest(self) -> float | None:
        manifest_path = self.input_path / "manifest.json"
        if not manifest_path.exists():
            return None
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            images = data.get("images", [])
            if len(images) >= 2:
                t0 = float(images[0]["time_sec"])
                t1 = float(images[1]["time_sec"])
                if t1 > t0:
                    return 1.0 / (t1 - t0)
        except Exception:
            return None
        return None


def read_image_bgr(path: str | Path):
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def _quiet_opencv_video_logs() -> None:
    if hasattr(cv2, "setLogLevel"):
        cv2.setLogLevel(0)
