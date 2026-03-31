# 哈基米桌面宠物 MVP
## 基于"全链路自我验证"的桌面智能助手

> 记住我们将MVP的定义收敛为"你自己就是第一个、也是唯一一个必须满意的用户"。

---

## 🎯 项目简介

哈基米桌面宠物是一个轻量级的桌面智能助手，专注解决数字化办公场景下的三个核心痛点：

- **事务管理混乱** → 30秒内完成任务记录
- **隐私安全担忧** → 离开工位时自动保护隐私  
- **决策疲劳** → 10分钟内生成可执行的周末出行方案

## ✨ 核心功能

### 1. 智能事务管理 📝
- 自然语言任务输入（如"明天下午2点开会"）
- 智能时间解析和优先级判断
- 自动提醒和任务跟踪
- **成功指标**: 记录成功率>95%

### 2. 自动隐私保护 🔒
- 人脸检测技术监控用户状态
- 离开工位时自动锁屏保护
- 用户返回时自动解锁
- **成功指标**: 检测准确率>90%

### 3. 快速出行规划 ✈️
- 输入目的地、预算、天数即可
- 10分钟内生成2套完整出行方案
- 包含景点推荐、住宿、美食、交通
- **成功指标**: 方案生成时间<10分钟

### 4. 桌面陪伴交互 💬
- 可爱的哈基米形象在桌面活动
- 智能对话和情感支持
- 右键菜单快速访问功能
- **成功指标**: 用户满意度>80%

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Windows 10+ / macOS 10.14+ / Ubuntu 18.04+
- 摄像头设备（用于隐私保护功能）

### 安装步骤

1. **克隆项目**
```bash
git clone <项目地址>
cd WindowPet_MVP
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **测试模块**
```bash
python test_app.py
```

4. **启动应用**
```bash
python start.py
# 或者
python main.py
```

### 首次使用

1. 启动后，哈基米会出现在桌面右下角
2. 双击哈基米打开聊天对话框
3. 右键哈基米查看功能菜单
4. 系统托盘图标提供快速访问

## 📱 使用指南

### 任务管理
```
# 自然语言添加任务
"明天下午2点开会"
"下周一交报告，重要"
"提醒我买牛奶"
```

### 出行规划
```
# 在聊天框或出行规划对话框中输入
"我想去北京玩2天，预算1000元"
"上海3日游，喜欢美食和历史"
```

### 隐私保护
- 自动启用，无需手动操作
- 可在右键菜单中手动开关
- 检测到人脸离开30秒后自动锁屏

## 🏗️ 项目结构

```
WindowPet_MVP/
├── src/                    # 源代码
│   ├── ai/                # AI服务层
│   │   ├── nlp_processor.py      # 自然语言处理
│   │   ├── vision_detector.py    # 计算机视觉
│   │   └── dialogue_generator.py # 对话生成
│   ├── core/              # 业务逻辑层
│   │   ├── task_manager.py       # 事务管理器
│   │   ├── privacy_guard.py      # 隐私保护器
│   │   └── travel_planner.py     # 出行规划器
│   ├── ui/                # 用户界面层
│   │   ├── desktop_pet.py        # 桌面宠物主界面
│   │   └── dialogs.py            # 对话框组件
│   └── utils/             # 工具模块
│       ├── database.py           # 数据库管理
│       ├── config.py             # 配置管理
│       └── logger.py             # 日志系统
├── resource/              # 静态资源
│   ├── pic1-4.jpg        # 哈基米形象图片
│   ├── config.yaml       # 配置文件
│   └── .env.example      # 环境变量示例
├── data/                  # 数据目录
└── logs/                  # 日志目录
```

## 🔧 配置说明

### 基础配置 (resource/config.yaml)
```yaml
pet:
  name: "哈基米"
  images: ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg"]
  animation_speed: 2000

privacy:
  face_detection: true
  detection_interval: 2.0
  away_threshold: 30

features:
  task_manager: true
  privacy_guard: true
  travel_planner: true
  chat: true
```

### 环境变量 (.env)
```bash
# AI服务配置（可选）
DEEPSEEK_API_KEY=your_api_key_here

# 地图服务配置（可选）
AMAP_API_KEY=your_amap_key_here
```

## 📊 MVP验证指标

基于"自我验证"原则，我们设定了以下关键指标：

### 指标A：解决率 (Success Rate)
- **定义**: 每次使用产品时，成功解决当前问题的比例
- **目标**: ≥60%（合格工具标准）

### 指标B：复用率 (Retention)  
- **定义**: 解决第一次问题后，一周内自发再次使用的比例
- **目标**: ≥20%（高频工具标准）

### 指标C：不可替代性 (Stickiness)
- **定义**: 如果产品消失，用户感到"非常失望"的程度
- **目标**: ≥70%用户表示"非常失望"

## 🐛 故障排除

### 常见问题

1. **无法启动应用**
   ```bash
   # 检查Python版本
   python --version
   
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

2. **摄像头无法访问**
   - 检查摄像头权限设置
   - 确认摄像头未被其他应用占用
   - 可在配置中禁用人脸检测功能

3. **任务提醒不工作**
   - 检查系统通知权限
   - 确认应用在后台运行
   - 查看日志文件排查问题

### 日志查看
```bash
# 查看应用日志
tail -f logs/hakimi_pet.log
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 基于"全链路自我验证"的MVP设计理念
- 感谢开源社区提供的技术支持
- 感谢所有测试用户的反馈和建议

---

**如果这个产品连你自己（最挑剔的用户）都不愿意连续用一周，那它绝不可能推广给别人。**

*让我们先做一个自己也许能用一辈子的好工具，再谈它是不是个好产品。*