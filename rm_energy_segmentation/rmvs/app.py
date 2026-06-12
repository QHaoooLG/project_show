from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2

from .infer import load_model, predict_frame
from .paths import default_model_path, default_video_path, ensure_dir
from .tracker import EnergyTracker
from .video_io import FrameSource
from .visualize import draw_visualization
from .utils import write_json


@dataclass(slots=True)
class RecognitionConfig:
    model_path: Path = default_model_path()
    input_path: Path = default_video_path()
    output_dir: Path = Path("outputs/video_default")
    threshold: float = 0.45
    min_area: int = 80
    max_area_ratio: float = 0.55
    device: str = "cpu"
    process_every: int = 1
    max_frames: int = 0
    resize_width: int = 720
    no_window: bool = False
    save_video: bool = True
    output_fps: float = 0.0
    use_warm_gate: bool = True
    max_instances: int = 6
    max_display_instances: int = 6
    instance_max_aspect_ratio: float = 6.0
    include_contours: bool = False


def run_recognition(config: RecognitionConfig) -> dict[str, Any]:
    if not Path(config.model_path).exists():
        raise FileNotFoundError(f"Model not found: {config.model_path}")
    source = FrameSource(config.input_path)
    output_dir = ensure_dir(config.output_dir)
    model, checkpoint, device = load_model(config.model_path, device=config.device)
    tracker = EnergyTracker()
    jsonl_path = output_dir / "frame_results.jsonl"
    video_path = output_dir / "annotated.mp4"
    writer = None
    processed = 0
    total_detections = 0
    started = time.perf_counter()
    last_frame_time = started

    print(
        f"[video] input={config.input_path} kind={source.kind} fps={source.fps:.2f} "
        f"frames={source.frame_count} model={config.model_path}",
        flush=True,
    )

    with jsonl_path.open("w", encoding="utf-8") as f:
        for packet in source:
            if config.max_frames > 0 and processed >= config.max_frames:
                break
            if packet.index % max(1, config.process_every) != 0:
                continue

            frame = _resize_frame(packet.frame_bgr, config.resize_width)
            loop_started = time.perf_counter()
            prediction = predict_frame(
                model,
                checkpoint,
                device,
                frame,
                frame_index=packet.index,
                time_sec=packet.time_sec,
                threshold=config.threshold,
                min_area=config.min_area,
                max_area_ratio=config.max_area_ratio,
                use_warm_gate=config.use_warm_gate,
                max_instances=config.max_instances,
                max_aspect_ratio=config.instance_max_aspect_ratio,
                include_contours=config.include_contours,
            )
            tracking = tracker.update(prediction.detections, time_sec=packet.time_sec, frame_shape=frame.shape)
            now = time.perf_counter()
            processing_fps = 1.0 / max(1e-6, now - last_frame_time)
            last_frame_time = now
            visual = None
            if config.save_video or not config.no_window:
                visual = draw_visualization(
                    frame,
                    prediction,
                    tracking,
                    input_fps=source.fps,
                    processing_fps=processing_fps,
                    threshold=config.threshold,
                    min_area=config.min_area,
                    max_display_instances=config.max_display_instances,
                )

            if config.save_video:
                if visual is None:
                    raise RuntimeError("Visualization frame was not created for video output.")
                if writer is None:
                    fps = config.output_fps if config.output_fps > 0 else max(1.0, source.fps / max(1, config.process_every))
                    writer = _video_writer(video_path, fps=fps, frame_size=(visual.shape[1], visual.shape[0]))
                writer.write(visual)

            record = prediction.to_dict()
            record["source_name"] = packet.source_name
            record["tracking"] = tracking.to_dict()
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            processed += 1
            total_detections += len(prediction.detections)

            if processed == 1 or processed % 10 == 0:
                print(
                    f"[video] frame={packet.index} processed={processed} "
                    f"detections={len(prediction.detections)} infer={prediction.inference_time_ms:.1f}ms "
                    f"loop={((time.perf_counter() - loop_started) * 1000.0):.1f}ms",
                    flush=True,
                )

            if not config.no_window:
                if visual is None:
                    raise RuntimeError("Visualization frame was not created for display output.")
                cv2.imshow("RoboMaster Energy Instance Segmentation", visual)
                key = cv2.waitKey(max(1, int(1000 / max(source.fps, 1.0)))) & 0xFF
                if key in (27, ord("q")):
                    break

    if writer is not None:
        writer.release()
    if not config.no_window:
        cv2.destroyAllWindows()

    elapsed = time.perf_counter() - started
    summary = {
        "input_path": str(config.input_path),
        "model_path": str(config.model_path),
        "output_dir": str(output_dir),
        "annotated_video": str(video_path) if config.save_video else None,
        "frame_results": str(jsonl_path),
        "processed_frames": processed,
        "total_detections": total_detections,
        "avg_detections_per_frame": total_detections / max(1, processed),
        "elapsed_sec": elapsed,
        "avg_processing_fps": processed / max(1e-6, elapsed),
        "config": _serializable_config(config),
    }
    write_json(output_dir / "summary.json", summary)
    print(
        f"[video] complete: processed={processed} avg_fps={summary['avg_processing_fps']:.2f} "
        f"output={output_dir}",
        flush=True,
    )
    return summary


def _resize_frame(frame, resize_width: int):
    if resize_width <= 0:
        return frame
    height, width = frame.shape[:2]
    scale = resize_width / width
    return cv2.resize(frame, (resize_width, max(1, int(round(height * scale)))), interpolation=cv2.INTER_AREA)


def _video_writer(path: Path, *, fps: float, frame_size: tuple[int, int]) -> cv2.VideoWriter:
    path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, frame_size)
    if not writer.isOpened():
        raise ValueError(f"Cannot create video writer: {path}")
    return writer


def _serializable_config(config: RecognitionConfig) -> dict[str, Any]:
    data = asdict(config)
    data["model_path"] = str(config.model_path)
    data["input_path"] = str(config.input_path)
    data["output_dir"] = str(config.output_dir)
    return data
