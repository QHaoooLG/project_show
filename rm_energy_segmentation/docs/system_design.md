# 基于实例分割的能量机关视频实时识别系统设计方案

## 1. 建设目标

本系统面向 RoboMaster 2023 机甲大师超级对抗赛能量机关视觉识别场景，在 `rm_energy_segmentation/` 中实现从图片数据集训练实例分割模型，再对能量机关视频进行实时识别、实例分割可视化、语义目标管理和装甲模块参数估计的工程闭环。

当前系统重心为“图像实例分割技术在能量机关识别中的应用”。系统不再设计未来点位外推算法，而是围绕实例分割结果输出如下视觉参数：

- 能量机关中心位置；
- 中心 R 标实例；
- 主亮装甲模块实例；
- 装甲模块参考点；
- 模块数量与整体状态；
- 基于 Ceres 风格圆拟合得到的半径、角度、角速度和拟合误差；
- 实时视频识别 FPS、分割概率、实例数量和语义框统计。

## 2. 场景约束

依据 RoboMaster 2023 能量机关规则，视觉识别系统重点关注以下对象和状态：

- 能量机关由中心 R 标、支架和 5 个装甲模块组成；
- 能量机关存在不可激活、可激活、正在激活、已激活和激活失败等状态；
- 小能量机关固定转速，大能量机关按周期函数变速；
- 正在激活阶段存在随机点亮装甲模块；
- 五个支架全部点亮后进入整体激活状态。

因此，系统输出不应停留在整图分类，而应以实例分割为核心，提供每个可见实例的 mask、bbox、中心点、面积、置信度、语义角色和模块参数。

## 3. 数据输入设计

### 3.1 默认训练图片数据集

默认训练数据：

```text
data\关灯红方小能量机关激活全过程_frame_dataset
```

该目录由视频抽帧工具生成，当前结构为：

```text
关灯红方小能量机关激活全过程_frame_dataset/
├── images/
├── manifest.json
├── manifest.csv
└── preview_contact_sheet.jpg
```

当前数据集中没有人工实例 mask 或 YOLO 分割标签。为保证系统可以直接训练，本系统采用“高亮能量机关区域伪 mask 生成”的弱监督训练方案，并在伪 mask 中加入去噪约束。

### 3.2 视频识别输入

系统识别输入支持两类：

- 视频文件：如 `data\关灯红方小能量机关激活全过程.mp4`；
- 图片帧目录：如 `data\关灯红方小能量机关激活全过程_frame_dataset`。

当输入为目录时，系统按文件名顺序读取 `images/` 下图片，以近似实时方式进行播放和识别；当输入为视频文件时，通过 OpenCV 逐帧读取。

## 4. 总体架构

| 模块 | 作用 |
|---|---|
| `rmvs.paths` | 默认路径、输出目录和文件类型判断 |
| `rmvs.pseudo_label` | 基于颜色、亮度和主光簇过滤的能量机关伪 mask 生成 |
| `rmvs.dataset` | 图片数据集扫描、训练/验证划分、PyTorch Dataset |
| `rmvs.model` | Tiny U-Net 实例分割骨干网络 |
| `rmvs.train` | 训练循环、损失函数、指标、模型保存和实时训练日志 |
| `rmvs.infer` | 模型加载、单帧推理、暖色门控、连通域实例拆分和语义角色分配 |
| `rmvs.tracker` | Ceres 风格圆拟合、中心估计、角度估计和角速度估计 |
| `rmvs.video_io` | 视频文件和图片帧目录统一读取 |
| `rmvs.visualize` | 中心 R 标、装甲模块、能量机关整体识别框、Ceres 拟合圆和参数面板绘制 |
| `rmvs.app` | 识别流程编排、视频输出和 summary 生成 |
| `scripts/train_model.py` | 训练入口 |
| `scripts/run_video_recognition.py` | 视频/帧目录识别入口 |
| `scripts/run_gui.py` | 带可视化窗口的运行入口 |
| `scripts/run_tests.py` | 自动化测试入口 |

整体流程：

```text
图片数据集
  -> 伪 mask 生成
  -> Tiny U-Net 训练
  -> 单帧概率图推理
  -> 暖色门控去噪
  -> 连通域实例拆分
  -> 语义角色分配
  -> Ceres 风格模块参数估计
  -> 视频可视化与 JSON 输出
```

## 5. 算法设计

### 5.1 去噪伪 mask 生成

能量机关发光区域具有红、橙、黄高亮特征。系统先在 HSV 空间构建暖色候选：

```text
M_warm(x,y)=1, if hue is red/orange/yellow and saturation >= 85 and value >= 105
M_warm(x,y)=0, otherwise
```

对过曝亮核进行邻域约束，只有靠近暖色区域的亮核才保留：

```text
M_core(x,y)=1, if value >= 210 and near(M_warm)
M_raw = M_warm OR M_core
```

之后执行：

- 形态学闭运算连接断裂灯条；
- 形态学开运算去除孤立噪声；
- 主光簇保留，只保留面积最大的暖色光簇；
- 连通域组件过滤，约束最小面积、最大面积占比、最小框尺寸、最大长宽比和最小填充率。

该设计用于训练伪标签，同时也在推理时作为 `warm_gate` 门控过滤模型输出，可抑制绿色灯、蓝色反光和远离主能量机关区域的红色反光。

### 5.2 实例分割训练

模型采用 Tiny U-Net：

- 输入：RGB 图像，缩放到固定尺寸；
- 输出：背景/能量机关发光区域二分类 mask；
- 损失函数：BCEWithLogits + Dice Loss；
- 指标：验证集 foreground IoU。

训练目标：

```text
L = BCE(logits, M) + lambda * DiceLoss(sigmoid(logits), M)
lambda = 0.45
```

Dice Loss：

```text
DiceLoss = 1 - (2 * sum(P * M) + eps) / (sum(P) + sum(M) + eps)
```

### 5.3 推理阶段实例拆分

推理阶段对概率图执行：

1. sigmoid 得到前景概率；
2. 阈值化得到二值 mask；
3. 生成当前帧暖色去噪门控；
4. 将模型 mask 与暖色门控相交；
5. OpenCV 连通域拆分实例；
6. 过滤面积过小、面积占比过大、长宽比异常和填充率过低的候选；
7. 对明显过大的粘连连通域进行中心角向二次拆分；
8. 按语义优先级、`module_score` 和实例面积排序，最多保留 `max_instances=6` 个实例。

角向二次拆分用于解决多个装甲模块亮起后被支架灯条连接成大框的问题。系统提取过大候选中远离能量机关中心的外侧像素，按极角直方图寻找多个亮区，并将原 mask 中的像素分配到最近角向簇。若直方图被连续灯条粘连，则按角向跨度执行回退拆分。该策略只对 bbox 面积超过画面 10% 且角向跨度过大的候选启用。

默认关闭 `contour_xy` 输出。轮廓点仅在需要离线几何分析时通过 `--include-contours` 打开，以减少实时后处理开销。

### 5.4 识别框语义管理

系统为每个实例赋予语义角色：

| 内部角色 | 可视化标签 | 含义 |
|---|---|---|
| `active_armor` | `ACTIVE_ARMOR` | 主亮装甲模块 |
| `armor_module` | `ARMOR` | 装甲模块 |
| `center_r` | `CENTER_R` | 中心 R 标 |
| `whole_mechanism` | `WHOLE_MECHANISM` | 能量机关整体 |
| `light_candidate` | `LIGHT` | 低优先级灯光候选 |

角色分配策略：

- 通过实例面积加权中心估计能量机关整体中心；
- 选择靠近整体中心且面积合理的候选作为中心 R 标，过小碎片不再参与中心 R 标选择；
- 在非中心候选中筛选装甲模块形态目标；
- 沿能量机关中心到候选实例外侧方向估计模块参考点 `module_point_xy`；
- 统计模块参考点附近的主亮标识密度，得到 `module_score`；
- `module_score` 最高且满足阈值要求的模块标记为 `active_armor`；
- 其他装甲模块候选作为 `armor_module`；
- 当装甲模块大范围整体亮起时，合成 `whole_mechanism` 整体框。

可视化默认只绘制 `active_armor`、`armor_module`、`center_r`、`whole_mechanism` 和由 Ceres 风格圆拟合得到的 1 像素拟合圆，避免大量小灯点遮挡画面。

### 5.5 Ceres 风格参数估计

本系统的参数估计借鉴 Ceres Solver 的残差块建模方式。给定分割得到的模块参考点：

```text
p_i = (x_i, y_i)
```

需要估计圆心和半径：

```text
c = (c_x, c_y), R
```

残差定义为点到圆的径向误差：

```text
r_i = ||p_i - c||_2 - R
```

优化目标：

```text
minimize sum_i r_i^2
```

雅可比矩阵单行：

```text
J_i = [(c_x - x_i) / d_i, (c_y - y_i) / d_i, -1]
d_i = ||p_i - c||_2
```

Gauss-Newton 更新：

```text
(J^T J + lambda I) delta = -J^T r
[c_x, c_y, R] = [c_x, c_y, R] + delta
```

拟合完成后输出均方根误差：

```text
fit_error_px = sqrt(mean(r_i^2))
```

当迭代结果出现圆心大幅偏离初始中心、半径异常增大或误差恶化时，系统回退到初始中心和中位半径，避免模块参数在少数异常帧中发散。

若存在主亮装甲模块，则估计模块角度：

```text
theta = atan2(y_module - c_y, x_module - c_x)
```

角速度根据短时历史角度差估计：

```text
omega = wrap(theta_t - theta_{t-k}) / (t - t_k)
```

该部分只描述图像平面的模块运动参数，不承担外部执行决策。

## 6. 可视化界面设计

运行界面采用 OpenCV 窗口，显示内容包括：

- 当前视频帧；
- 中心 R 标识别框；
- 装甲模块识别框；
- 能量机关整体识别框；
- 基于当前帧 Ceres 风格参数估计结果的细线拟合圆；
- 薄线 bbox 和语义标签；
- 右侧参数面板。

右侧参数面板重新分为三组：

| 分组 | 展示内容 |
|---|---|
| `RUN` | frame/time、input FPS、processing FPS、inference time |
| `SEGMENTATION` | detections、role counts、probability、threshold、min area |
| `MODULE PARAMETERS` | status、center、module point、radius、angle、omega、fit error、module score、area、whole flag |

参数栏宽度固定为 500 像素，行距和字体已压缩，适配默认 `resize_width=720` 后的 404 像素画面高度，避免底部参数被截断。

## 7. 性能优化设计

当前优化点：

- 默认 `resize_width=720`，降低 CPU 推理、绘制和视频编码成本；
- 默认开启 `warm_gate`，减少无效连通域数量；
- 默认 `max_instances=6`，限制后处理和 JSON 输出规模；
- 默认 `max_display_instances=6`，降低绘制负载；
- 默认不提取轮廓点，避免 `findContours` 带来的额外耗时；
- 仅对明显过大的粘连连通域执行角向拆分，降低多模块亮起后的大框漂移；
- 左侧画面不再绘制半透明 mask 和点位标记，仅保留语义识别框与 1 像素 Ceres 拟合圆，降低遮挡并保留模块参数直观表达；
- 仅对少量模块点做 Ceres 风格圆拟合，迭代次数固定在 5 次以内；
- 参数栏简化为三组关键指标，提高实时观察效率。

本机实验中，完整 mp4 纯算法模式处理 `586` 帧，平均约 `24.26 FPS`；覆盖多模块后段的标注视频处理 `430` 帧，平均约 `22.79 FPS`。三个及以上模块亮起阶段，异常大框数量从优化前 `51` 帧降为 `0` 帧。

## 8. 输出设计

训练输出：

```text
outputs\train_filtered/
├── best_model.pt
├── last_model.pt
├── metrics.json
├── training_config.json
└── dataset_manifest.json
```

识别输出：

```text
outputs\video_mp4_module_params/
├── annotated.mp4
├── frame_results.jsonl
└── summary.json
```

`frame_results.jsonl` 保留每帧实例列表和参数估计结果。实例中包含 `role`、`role_name`、`module_point_xy` 和 `module_score`，参数估计中包含 `mechanism_center`、`fitted_radius`、`module_angle_deg`、`angular_velocity_deg_s` 和 `fit_error_px`。

## 9. 局限与扩展

- 当前训练数据来自无人工标注抽帧，伪 mask 不等同于人工精标实例 mask。
- 语义角色由启发式规则分配，在遮挡、过曝和非典型姿态下仍可能误分。
- 当前圆拟合在图像平面完成，未接入相机标定、三维位姿和外部控制模块。
- 后续可接入人工实例 mask、`data\XJTLU_2023_WIN_ALL` 标签数据或更强分割模型，以提高泛化能力和边界质量。
