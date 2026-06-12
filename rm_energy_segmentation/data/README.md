# Data Directory

This directory is intentionally kept out of version control except for this note.

Put local datasets or raw videos here when running the project, for example:

```text
data/
├── energy_demo.mp4
└── energy_demo_frame_dataset/
    ├── images/
    ├── manifest.json
    ├── manifest.csv
    └── preview_contact_sheet.jpg
```

The default scripts still support the original local RoboMaster demo names:

```text
data/关灯红方小能量机关激活全过程.mp4
data/关灯红方小能量机关激活全过程_frame_dataset/
```

Large videos, image datasets, trained models, and generated outputs should not be committed to GitHub. Use the commands in the root `README.md` to regenerate them locally.

