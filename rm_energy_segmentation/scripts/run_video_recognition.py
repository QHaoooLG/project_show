from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from rmvs.app import RecognitionConfig, run_recognition
from rmvs.paths import default_model_path, default_video_path, outputs_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run video/frame-directory energy mechanism recognition.")
    parser.add_argument("--model", default=str(default_model_path()))
    parser.add_argument("--input", default=str(default_video_path()))
    parser.add_argument("--output-dir", default=str(outputs_dir() / "video_default"))
    parser.add_argument("--threshold", type=float, default=0.45)
    parser.add_argument("--min-area", type=int, default=80)
    parser.add_argument("--max-area-ratio", type=float, default=0.55)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--process-every", type=int, default=1)
    parser.add_argument("--max-frames", type=int, default=0)
    parser.add_argument("--resize-width", type=int, default=720)
    parser.add_argument("--max-instances", type=int, default=6)
    parser.add_argument("--max-display-instances", type=int, default=6)
    parser.add_argument("--instance-max-aspect-ratio", type=float, default=6.0)
    parser.add_argument("--no-warm-gate", action="store_true")
    parser.add_argument("--include-contours", action="store_true")
    parser.add_argument("--no-window", action="store_true")
    parser.add_argument("--no-save-video", action="store_true")
    parser.add_argument("--output-fps", type=float, default=0.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_recognition(
        RecognitionConfig(
            model_path=Path(args.model),
            input_path=Path(args.input),
            output_dir=Path(args.output_dir),
            threshold=args.threshold,
            min_area=args.min_area,
            max_area_ratio=args.max_area_ratio,
            device=args.device,
            process_every=args.process_every,
            max_frames=args.max_frames,
            resize_width=args.resize_width,
            no_window=args.no_window,
            save_video=not args.no_save_video,
            output_fps=args.output_fps,
            use_warm_gate=not args.no_warm_gate,
            max_instances=args.max_instances,
            max_display_instances=args.max_display_instances,
            instance_max_aspect_ratio=args.instance_max_aspect_ratio,
            include_contours=args.include_contours,
        )
    )
    print(f"summary={summary['output_dir']}")


if __name__ == "__main__":
    main()
