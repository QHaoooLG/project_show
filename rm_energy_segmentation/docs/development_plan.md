# rm_energy_segmentation 代码开发方案

## 1. 开发原则

- 所有系统代码和工程文件均位于 `rm_energy_segmentation/`。
- 优先保证从训练到视频识别的闭环可运行，再扩展模型复杂度。
- 图像识别核心必须是实例分割，输出 mask、bbox、center、score、role、module_point_xy 和 module_score。
- 装甲模块参数估计基于 Ceres 风格最小二乘圆拟合，不包含未来点位外推。
- 命令默认从 `rm_energy_segmentation` 根目录运行，示例命令全部采用 PowerShell 可直接执行的写法。
- 默认训练数据使用 `data\关灯红方小能量机关激活全过程_frame_dataset`。
- 默认模型输出使用 `outputs\train_filtered`。
- 默认视频识别支持 `data\关灯红方小能量机关激活全过程.mp4` 和抽帧目录输入。
- 自动测试和实验命令可复现，输出集中写入 `outputs/`。

## 2. 项目结构

```text
rm_energy_segmentation/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .editorconfig
├── .gitignore
├── data/
│   └── README.md
├── docs/
│   ├── assets/
│   ├── system_design.md
│   └── development_plan.md
├── rmvs/
│   ├── __init__.py
│   ├── paths.py
│   ├── pseudo_label.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── infer.py
│   ├── tracker.py
│   ├── video_io.py
│   ├── visualize.py
│   └── app.py
├── scripts/
│   ├── train_model.py
│   ├── run_video_recognition.py
│   ├── run_gui.py
│   └── run_tests.py
├── test/
│   ├── test_pipeline.py
│   ├── test_pseudo_label.py
│   ├── test_module_parameters.py
│   └── test_visualize.py
├── tools/
│   ├── README.md
│   └── extract_video_frames.py
└── outputs/
    └── README.md
```

## 3. 已完成阶段

### 阶段 A：项目规范化

1. 新增 `.editorconfig`、`.gitignore`、`requirements.txt`、`pyproject.toml`。
2. 创建 `rmvs/`、`scripts/`、`test/`、`tools/` 和 `outputs/`。
3. 写入默认路径、输出目录和文件类型判断工具。

验收方式：

```powershell
python -m py_compile (Get-ChildItem -Path rmvs,scripts,test,tools -Recurse -Filter *.py | ForEach-Object { $_.FullName })
```

### 阶段 B：伪 mask 数据集

1. 扫描 `frame_dataset/images`。
2. 基于 HSV 红、橙、黄高亮区域生成伪 mask。
3. 引入亮核邻域约束、主光簇保留和连通域几何过滤。
4. 实现 PyTorch Dataset。
5. 编写测试验证伪 mask 对绿色、蓝色灯光干扰的过滤能力。

验收标准：

- 对抽帧样例能生成非空 mask。
- 绿色安全通道灯和蓝色反光灯不会被保留为目标 mask。
- 主能量机关光簇优先于孤立红色反光。

### 阶段 C：实例分割训练

1. 实现 Tiny U-Net 二分类分割模型。
2. 实现 BCE + Dice Loss。
3. 实现训练/验证划分、实时训练日志、模型保存。
4. 输出 `best_model.pt`、`last_model.pt`、`metrics.json`、`training_config.json`。
5. 默认训练输出目录调整为 `outputs\train_filtered`。

验收标准：

- 小样本少量 epoch 可完成训练并保存模型。
- 默认抽帧数据训练后生成 `outputs\train_filtered\best_model.pt`。
- `metrics.json` 中包含训练损失、验证损失和验证 IoU。

### 阶段 D：单帧实例推理

1. 加载训练模型。
2. 对单帧图像输出概率图。
3. 推理阶段生成暖色去噪门控。
4. 阈值化、门控相交和连通域拆分实例。
5. 输出实例 mask、bbox、center、score、area。
6. 为实例分配 `active_armor`、`armor_module`、`center_r`、`whole_mechanism`、`light_candidate` 角色。
7. 估计模块参考点 `module_point_xy` 和模块分数 `module_score`。
8. 默认不提取 `contour_xy`，需要时通过 `--include-contours` 打开。
9. 对明显过大的粘连连通域执行中心角向二次拆分，避免多模块亮起后生成横跨多个装甲模块的大框。

验收标准：

- 对样例图片能得到语义化实例结果或明确空结果。
- 逐帧 JSON 中包含 `role`、`role_name`、`module_point_xy` 和 `module_score` 字段。
- 整体亮起状态下生成 `whole_mechanism`。

### 阶段 E：视频实时识别与模块参数估计

1. 统一读取视频文件或图片帧目录。
2. 默认使用 `resize_width=720` 提升 CPU 推理速度。
3. 逐帧执行实例分割推理和语义过滤。
4. 使用 Ceres 风格残差 `r_i = ||p_i - c|| - R` 拟合能量机关圆参数。
5. 输出中心、半径、模块角度、角速度、拟合误差和模块状态。
6. 绘制中心 R 标、装甲模块、能量机关整体的薄线识别框和 1 像素 Ceres 拟合圆，并保留右侧参数栏。
7. 保存 `annotated.mp4`、`frame_results.jsonl`、`summary.json`。

验收标准：

- 默认 mp4 和帧目录均能运行完整流程。
- 无 GUI 场景中 `--no-window` 可保存结果。
- 可视化画面不被大量灯光候选框遮挡。
- 右侧参数栏完整显示 RUN、SEGMENTATION、MODULE PARAMETERS 三组信息。
- 平均 FPS 相比上一版规则目标流程提升。

### 阶段 F：文档与最终验证

1. 更新 `README.md`。
2. 更新 `系统设计方案.md`。
3. 更新 `代码开发方案.md`。
4. 运行编译检查。
5. 运行自动化测试。
6. 运行识别脚本帮助信息检查。
7. 运行帧目录和 mp4 识别实验。
8. 生成并检查标注视频预览图。

验收标准：

- README 覆盖算法设计、运行流程、系统运行指南、语义框含义、去噪参数和优化实验结果。
- 文档中的示例命令可直接在 PowerShell 中运行。
- 代码中不暴露旧版提前量参数。
- 所有验证命令通过。

## 4. 推荐命令

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

训练优化模型：

```powershell
python scripts\train_model.py --dataset-dir data\关灯红方小能量机关激活全过程_frame_dataset --output-dir outputs\train_filtered --epochs 10 --batch-size 2 --image-size 128 --base-channels 10 --val-ratio 0.2 --progress-interval 5
```

推荐正式训练参数：`--epochs 6` 到 `10`、`--batch-size 2`、`--image-size 128` 或 `160`、`--base-channels 8` 或 `12`、`--val-ratio 0.2`。当前抽帧数据只有 40 张，训练轮数过高容易让伪 mask 噪声被模型记住，建议以验证集 IoU、视频可视化效果和模块稳定性共同选择模型。

对原始视频识别并保存结果：

```powershell
python scripts\run_video_recognition.py --model outputs\train_filtered\best_model.pt --input data\关灯红方小能量机关激活全过程.mp4 --output-dir outputs\video_mp4_module_params --threshold 0.35 --min-area 25 --max-area-ratio 0.65 --resize-width 720 --max-frames 120 --max-instances 6 --max-display-instances 6 --no-window
```

对用户指定的帧目录识别：

```powershell
python scripts\run_video_recognition.py --model outputs\train_filtered\best_model.pt --input data\关灯红方小能量机关激活全过程_frame_dataset --output-dir outputs\frame_dir_module_params --threshold 0.35 --min-area 35 --max-area-ratio 0.65 --max-instances 6 --max-display-instances 6 --no-window
```

带窗口运行：

```powershell
python scripts\run_gui.py --model outputs\train_filtered\best_model.pt --input data\关灯红方小能量机关激活全过程.mp4 --threshold 0.35 --min-area 25 --resize-width 720
```

纯性能测试可跳过可视化绘制和标注视频编码：

```powershell
python scripts\run_video_recognition.py --model outputs\train_filtered\best_model.pt --input data\关灯红方小能量机关激活全过程.mp4 --output-dir outputs\video_fast_no_video --threshold 0.35 --min-area 25 --resize-width 640 --max-instances 5 --max-display-instances 5 --no-window --no-save-video
```

运行测试：

```powershell
python scripts\run_tests.py
```

运行编译检查：

```powershell
python -m py_compile (Get-ChildItem -Path rmvs,scripts,test,tools -Recurse -Filter *.py | ForEach-Object { $_.FullName })
```

查看识别入口参数：

```powershell
python scripts\run_video_recognition.py --help
```

## 5. 优化实验记录

| 实验 | 上一版规则目标流程 | 当前模块参数版本 |
|---|---:|---:|
| 帧目录平均检测数/帧 | 3.45 | 3.00 |
| 帧目录平均 FPS | 10.46 | 16.64 |
| mp4 平均检测数/帧 | 3.11 | 2.325 |
| mp4 平均 FPS | 15.75 | 22.79 |
| 自动测试数量 | 8 | 10 |

补充：完整 mp4 输入在 `--no-window --no-save-video` 纯算法模式下处理 `586` 帧，平均约 `24.26 FPS`。

多装甲模块稳定性实验：

| 指标 | 优化前 | 优化后 |
|---|---:|---:|
| 三个及以上模块亮起阶段最大 bbox 面积 | 90597 | 43554 |
| bbox 面积超过 50000 的异常大框帧数 | 51 | 0 |
| 参数中心出界帧数 | 未统计 | 0 |

当前版本输出目录：

- `outputs\frame_dir_module_params`
- `outputs\video_mp4_module_params`

当前版本预览图：

- `outputs\video_mp4_module_params\preview_module_params_040.jpg`
- `outputs\video_mp4_module_params\preview_module_params_100.jpg`
- `outputs\video_mp4_module_params\preview_module_params_119.jpg`
- `outputs\frame_dir_module_params\preview_module_params_020.jpg`
- `outputs\frame_dir_module_params\preview_module_params_039.jpg`

## 6. 风险与处理

| 风险 | 影响 | 处理 |
|---|---|---|
| 抽帧数据无人工标注 | 监督信号弱 | 使用暖色去噪伪 mask 训练，并在 README 中说明局限 |
| 小数据集仅 40 张 | 泛化能力有限 | 默认训练用于视频闭环演示，保留后续接入 XJTLU 标签数据接口 |
| 绿色/蓝色场地灯干扰 | 误检非目标灯光 | HSV 暖色门控直接排除非暖色灯光 |
| 真人红色反光干扰 | 误检孤立红色区域 | 主光簇保留、面积/长宽比/填充率过滤 |
| 模块语义误分 | 参数估计不稳定 | 使用中心约束、模块参考点评分和少量历史角度稳定约束 |
| GUI 在无显示环境中不可用 | 自动测试失败 | 所有视频识别命令支持 `--no-window` |
| 视频路径和帧目录路径混用 | 用户输入可能是目录 | `video_io` 同时支持视频文件和 `images/` 目录 |
| CPU 实时推理较慢 | 帧率下降 | 默认宽度 720，支持 `--process-every`、`--max-instances`、`--max-display-instances`；纯算法测试可组合 `--no-window --no-save-video` |
