# Tools

Utilities for preparing local RoboMaster energy-mechanism datasets.

## `extract_video_frames.py`

Extract sampled frames from a video and create an image dataset directory.

Default input:

```text
data/关灯红方小能量机关激活全过程.mp4
```

Default output:

```text
data/关灯红方小能量机关激活全过程_frame_dataset
```

Install dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

Basic usage:

```powershell
python tools/extract_video_frames.py --video data/energy_demo.mp4 --output-dir data/energy_demo_frame_dataset --frame-step 15 --overwrite
```

Common options:

| Option | Default | Description |
|---|---:|---|
| `--video` | default demo video | Input video path |
| `--output-dir` | `data/<video>_frame_dataset` | Output dataset directory |
| `--frame-step` | `15` | Save one frame every N frames |
| `--time-step` | `0` | Save one frame every N seconds; overrides `--frame-step` when greater than 0 |
| `--max-images` | `0` | Maximum exported images; 0 means unlimited |
| `--format` | `jpg` | Output format, `jpg` or `png` |
| `--overwrite` | off | Replace an existing non-empty output directory |
| `--no-preview` | off | Skip `preview_contact_sheet.jpg` generation |

Generated dataset:

```text
energy_demo_frame_dataset/
├── images/
├── manifest.json
├── manifest.csv
└── preview_contact_sheet.jpg
```

