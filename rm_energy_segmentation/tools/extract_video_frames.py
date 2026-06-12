from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import cv2
from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_VIDEO = DATA_DIR / "关灯红方小能量机关激活全过程.mp4"


@dataclass(frozen=True, slots=True)
class FrameRecord:
    index: int
    frame_index: int
    time_sec: float
    image_path: str
    width: int
    height: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract sampled video frames into an image dataset.",
    )
    parser.add_argument("--video", default=str(DEFAULT_VIDEO), help="Input video path.")
    parser.add_argument("--output-dir", default=None, help="Output dataset directory.")
    parser.add_argument("--frame-step", type=int, default=15, help="Extract one frame every N frames.")
    parser.add_argument(
        "--time-step",
        type=float,
        default=0.0,
        help="Extract one frame every N seconds. Overrides --frame-step when > 0.",
    )
    parser.add_argument("--start-frame", type=int, default=0, help="First frame index to consider.")
    parser.add_argument("--end-frame", type=int, default=-1, help="Last frame index to consider, inclusive.")
    parser.add_argument("--max-images", type=int, default=0, help="Maximum images to export. 0 means no limit.")
    parser.add_argument("--prefix", default="frame", help="Output image filename prefix.")
    parser.add_argument("--format", choices=("jpg", "png"), default="jpg", help="Output image format.")
    parser.add_argument("--jpeg-quality", type=int, default=95, help="JPEG quality, used only for jpg output.")
    parser.add_argument("--resize-width", type=int, default=0, help="Optional output width.")
    parser.add_argument("--resize-height", type=int, default=0, help="Optional output height.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing non-empty output directory.")
    parser.add_argument("--no-preview", action="store_true", help="Do not create preview_contact_sheet.jpg.")
    parser.add_argument("--preview-columns", type=int, default=6, help="Columns in preview contact sheet.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    video_path = Path(args.video).resolve()
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_dir = Path(args.output_dir).resolve() if args.output_dir else default_output_dir(video_path)
    image_dir = prepare_output_dir(output_dir, overwrite=args.overwrite)

    info = read_video_info(video_path)
    frame_indices = build_frame_indices(
        total_frames=info["frame_count"],
        fps=info["fps"],
        frame_step=args.frame_step,
        time_step=args.time_step,
        start_frame=args.start_frame,
        end_frame=args.end_frame,
        max_images=args.max_images,
    )
    if not frame_indices:
        raise ValueError("No frame indices selected. Check start/end/step arguments.")

    print(
        "[extract] video="
        f"{video_path} fps={info['fps']:.3f} frames={info['frame_count']} "
        f"size={info['width']}x{info['height']}",
        flush=True,
    )
    print(
        f"[extract] output={output_dir} selected_frames={len(frame_indices)} format={args.format}",
        flush=True,
    )

    records = extract_frames(
        video_path=video_path,
        image_dir=image_dir,
        frame_indices=frame_indices,
        fps=info["fps"],
        prefix=args.prefix,
        image_format=args.format,
        jpeg_quality=args.jpeg_quality,
        resize_width=args.resize_width,
        resize_height=args.resize_height,
    )
    write_manifest(output_dir, video_path, info, args, records)
    if not args.no_preview:
        create_preview_contact_sheet(
            output_dir / "preview_contact_sheet.jpg",
            [Path(record.image_path) for record in records],
            columns=args.preview_columns,
        )
    print(f"[extract] complete: images={len(records)} dataset={output_dir}", flush=True)


def default_output_dir(video_path: Path) -> Path:
    safe_name = f"{video_path.stem}_frame_dataset"
    return video_path.parent / safe_name


def prepare_output_dir(output_dir: Path, *, overwrite: bool) -> Path:
    image_dir = output_dir / "images"
    if output_dir.exists() and any(output_dir.iterdir()):
        if not overwrite:
            raise FileExistsError(
                f"Output directory is not empty: {output_dir}. "
                "Use --overwrite or choose another --output-dir."
            )
        shutil.rmtree(output_dir)
    image_dir.mkdir(parents=True, exist_ok=True)
    return image_dir


def read_video_info(video_path: Path) -> dict[str, float | int]:
    cap = cv2.VideoCapture(str(video_path))
    try:
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if fps <= 0 or frame_count <= 0:
            raise ValueError(f"Invalid video metadata: fps={fps}, frames={frame_count}")
        return {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration_sec": frame_count / fps,
        }
    finally:
        cap.release()


def build_frame_indices(
    *,
    total_frames: int,
    fps: float,
    frame_step: int,
    time_step: float,
    start_frame: int,
    end_frame: int,
    max_images: int,
) -> list[int]:
    start = max(0, start_frame)
    end = total_frames - 1 if end_frame < 0 else min(total_frames - 1, end_frame)
    if start > end:
        return []

    if time_step > 0:
        step = max(1, int(round(time_step * fps)))
    else:
        step = max(1, frame_step)

    indices = list(range(start, end + 1, step))
    if indices[-1] != end:
        indices.append(end)
    if max_images > 0:
        indices = indices[:max_images]
    return indices


def extract_frames(
    *,
    video_path: Path,
    image_dir: Path,
    frame_indices: Iterable[int],
    fps: float,
    prefix: str,
    image_format: str,
    jpeg_quality: int,
    resize_width: int,
    resize_height: int,
) -> list[FrameRecord]:
    cap = cv2.VideoCapture(str(video_path))
    records: list[FrameRecord] = []
    indices = list(frame_indices)
    try:
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        for output_index, frame_index in enumerate(indices, start=1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = cap.read()
            if not ok or frame is None:
                print(f"[extract] warning: failed to read frame {frame_index}", flush=True)
                continue

            frame = resize_frame(frame, resize_width=resize_width, resize_height=resize_height)
            height, width = frame.shape[:2]
            time_sec = frame_index / fps
            image_name = f"{prefix}_{output_index:05d}_f{frame_index:06d}_t{time_sec:07.3f}.{image_format}"
            image_path = image_dir / image_name
            write_image(image_path, frame, image_format=image_format, jpeg_quality=jpeg_quality)
            records.append(
                FrameRecord(
                    index=output_index,
                    frame_index=frame_index,
                    time_sec=time_sec,
                    image_path=str(image_path),
                    width=width,
                    height=height,
                )
            )
            if output_index == 1 or output_index == len(indices) or output_index % 10 == 0:
                print(
                    f"[extract] saved {output_index}/{len(indices)} "
                    f"frame={frame_index} time={time_sec:.3f}s path={image_path.name}",
                    flush=True,
                )
    finally:
        cap.release()
    return records


def resize_frame(frame, *, resize_width: int, resize_height: int):
    if resize_width <= 0 and resize_height <= 0:
        return frame
    height, width = frame.shape[:2]
    if resize_width > 0 and resize_height > 0:
        target_size = (resize_width, resize_height)
    elif resize_width > 0:
        scale = resize_width / width
        target_size = (resize_width, max(1, int(round(height * scale))))
    else:
        scale = resize_height / height
        target_size = (max(1, int(round(width * scale))), resize_height)
    return cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)


def write_image(image_path: Path, frame, *, image_format: str, jpeg_quality: int) -> None:
    if image_format == "jpg":
        params = [int(cv2.IMWRITE_JPEG_QUALITY), max(1, min(100, jpeg_quality))]
        extension = ".jpg"
    else:
        params = [int(cv2.IMWRITE_PNG_COMPRESSION), 3]
        extension = ".png"
    ok, encoded = cv2.imencode(extension, frame, params)
    if not ok:
        raise ValueError(f"Failed to encode image: {image_path}")
    image_path.write_bytes(encoded.tobytes())


def write_manifest(
    output_dir: Path,
    video_path: Path,
    video_info: dict[str, float | int],
    args: argparse.Namespace,
    records: list[FrameRecord],
) -> None:
    manifest = {
        "video_path": str(video_path),
        "video_info": video_info,
        "arguments": {
            "frame_step": args.frame_step,
            "time_step": args.time_step,
            "start_frame": args.start_frame,
            "end_frame": args.end_frame,
            "max_images": args.max_images,
            "format": args.format,
            "jpeg_quality": args.jpeg_quality,
            "resize_width": args.resize_width,
            "resize_height": args.resize_height,
        },
        "num_images": len(records),
        "images": [asdict(record) for record in records],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with (output_dir / "manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "frame_index", "time_sec", "image_path", "width", "height"],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def create_preview_contact_sheet(output_path: Path, image_paths: list[Path], *, columns: int) -> None:
    if not image_paths:
        return
    columns = max(1, columns)
    thumb_w, thumb_h = 240, 135
    label_h = 22
    rows = (len(image_paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for idx, image_path in enumerate(image_paths):
        row, col = divmod(idx, columns)
        x = col * thumb_w
        y = row * (thumb_h + label_h)
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            image.thumbnail((thumb_w, thumb_h))
            paste_x = x + (thumb_w - image.width) // 2
            paste_y = y + (thumb_h - image.height) // 2
            sheet.paste(image, (paste_x, paste_y))
        draw.text((x + 4, y + thumb_h + 4), image_path.stem[:32], fill=(20, 20, 20))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)


if __name__ == "__main__":
    main()
