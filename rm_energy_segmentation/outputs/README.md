# Outputs Directory

Generated training checkpoints and recognition outputs are written here.

Typical outputs:

```text
outputs/
├── train_filtered/
│   ├── best_model.pt
│   ├── last_model.pt
│   ├── metrics.json
│   └── training_config.json
└── video_default/
    ├── annotated.mp4
    ├── frame_results.jsonl
    └── summary.json
```

This directory is ignored by Git because model weights, videos, and frame-level JSON logs can become large quickly.

