# QHaoooLG 项目作品集

> 面向求职投递的项目展示仓库。  
> 重点展示我在 **C++/ROS2 机器人视觉**、**Java 后端开发**、**Python 桌面应用**、**Qt/C++ 面向对象开发** 和 **软件测试** 方向的实践经历。

## 个人定位

我是齐浩龙，山东理工大学计算机科学与技术专业本科生，2026 届应届生。我的项目经历主要集中在机器人视觉系统部署与调试、后端业务系统开发、桌面端应用工程化和自动化测试。

- **求职方向**：软件开发工程师 / 后端开发工程师 / C++ 算法或机器人软件开发相关岗位
- **核心能力**：C++、Java、Python、ROS2、OpenCV、Spring Boot、MyBatis-Plus、MySQL、Qt、JUnit
- **项目特点**：既有竞赛实车调试和团队协作经历，也有可运行的桌面应用、后端业务系统和测试工程实践
- **联系方式**：`qhaooolg@foxmail.com` / 微信 `QHaoooLG`

## 推荐阅读顺序

如果您来自招聘场景，建议按下面顺序快速浏览：

1. **机器人视觉/算法方向**：先看 [RM-QIQI-vision-main](./RM-QIQI-vision-main)，重点关注 ROS2 自瞄部署、相机接入、Foxglove 调试和部署手册。
2. **后端开发方向**：看 [TicketingSystem](./TicketingSystem)，重点关注 Spring Boot + MyBatis-Plus 的业务分层和票务管理流程。
3. **Python 应用方向**：看 [CubiclePal_MVP_v0](./CubiclePal_MVP_v0)，重点关注 PyQt5 桌面端、OpenCV 隐私检测、SQLite 数据管理和模块化结构。
4. **C++/Qt 基础方向**：看 [Zork-Qt-RPG](./Zork-Qt-RPG)，重点关注 OOP 建模、Qt GUI、游戏状态与交互逻辑。
5. **测试/质量方向**：看 [SoftwareTest](./SoftwareTest)，重点关注 JUnit、等价类、边界值、排序/搜索/日期逻辑测试。

## 项目一览

| 项目 | 方向 | 技术栈 | 我主要做了什么 | 推荐查看 |
|---|---|---|---|---|
| [RM-QIQI-vision-main](./RM-QIQI-vision-main) | 机器人视觉 / ROS2 | C++、ROS2、OpenCV、Foxglove、Hikvision SDK | 负责 RoboMaster 视觉自瞄系统部署、参数调试、相机接入验证、团队技术传承文档整理 | [部署手册](./RM-QIQI-vision-main/QIQI视觉避坑手册.pdf)、[演示视频](./RM-QIQI-vision-main/开源机器人自瞄项目部署效果实录.mp4) |
| [CubiclePal_MVP_v0](./CubiclePal_MVP_v0) | Python 桌面智能助手 | Python、PyQt5、OpenCV、SQLite、PyYAML | 设计 MVP 架构，实现桌面宠物、任务管理、隐私保护、出行规划、对话窗口和测试脚本 | [README](./CubiclePal_MVP_v0/README.md)、[项目文档](./CubiclePal_MVP_v0/doc/README.md) |
| [TicketingSystem](./TicketingSystem) | Java 后端 / 票务管理 | Java、Spring Boot、MyBatis-Plus、MySQL、Druid、Maven | 构建景区票务管理系统，覆盖用户、景点、票种、订单、支付、预约关系等业务模块 | [README](./TicketingSystem/README.md)、[主模块源码](./TicketingSystem/TicketingSystem_main/src/main/java/com/sdut) |
| [Zork-Qt-RPG](./Zork-Qt-RPG) | C++/Qt 游戏开发 | C++17、Qt Widgets、qmake | 实现房间地图、角色状态、道具系统、怪物战斗、随机传送、Qt 弹窗交互 | [README](./Zork-Qt-RPG/README.md)、[源码](./Zork-Qt-RPG/sourceFile) |
| [SoftwareTest](./SoftwareTest) | 软件测试 / 自动化测试 | Java、JUnit、Maven、Eclipse | 针对排序、搜索、日期计算、立方体体积等逻辑编写单元测试和边界/等价类测试 | [README](./SoftwareTest/README.md)、[A1 测试代码](./SoftwareTest/SoftwareTest_1/softwareTest_A1code/src/test/java)、[A2 测试代码](./SoftwareTest/SoftwareTest_2/softwareTest_A2code/src/test/java) |

## 技术栈概览

| 能力方向 | 关键词 | 对应项目 |
|---|---|---|
| 机器人视觉与部署 | ROS2 Humble、OpenCV、装甲板识别、PnP、扩展卡尔曼滤波、相机驱动、Foxglove 调试 | [RM-QIQI-vision-main](./RM-QIQI-vision-main) |
| 后端业务开发 | Spring Boot、MyBatis-Plus、MVC 分层、MySQL、Druid、Maven 多模块、登录/分页/文件上传 | [TicketingSystem](./TicketingSystem) |
| Python 桌面应用 | PyQt5、桌面宠物、系统托盘、SQLite、OpenCV 人脸检测、配置管理、日志、pytest 风格测试 | [CubiclePal_MVP_v0](./CubiclePal_MVP_v0) |
| C++/Qt 工程 | C++17、Qt Widgets、信号槽、OOP、游戏状态机、qmake | [Zork-Qt-RPG](./Zork-Qt-RPG) |
| 测试设计 | JUnit、断言、异常测试、参数化测试、边界值分析、等价类划分 | [SoftwareTest](./SoftwareTest) |

## 重点项目

### 1. RM-QIQI-vision-main：机器人装甲板自动瞄准系统部署

![RM-QIQI Vision demo](./RM-QIQI-vision-main/哨兵机器人旋转靶自瞄.png)

这是我最能体现工程落地能力的项目。项目围绕 RoboMaster 机器人视觉自瞄场景展开，核心目标是在 ROS2 环境下完成图像采集、装甲板识别、目标跟踪、解算与调试闭环。

**我的职责**

- 担任 RoboMaster 齐奇战队算法组组长，负责视觉自瞄系统部署、实车联调和组内研发推进。
- 基于 `rm_vision` / `rm_auto_aim` 等开源模块完成 ROS2 工作空间配置、Hikvision 工业相机接入、bringup 参数调试和运行链路验证。
- 使用 Foxglove Studio 查看图像、目标、TF/状态等调试数据，并结合实车表现修正识别与击打相关参数。
- 将部署踩坑、依赖安装、常见错误、相机配置和调试流程整理为 [QIQI 视觉避坑手册](./RM-QIQI-vision-main/QIQI视觉避坑手册.pdf)，用于战队后续技术传承。

**可验证内容**

- 自瞄系统演示：[开源机器人自瞄项目部署效果实录.mp4](./RM-QIQI-vision-main/开源机器人自瞄项目部署效果实录.mp4)
- 自瞄算法模块：[rm_auto_aim-main](./RM-QIQI-vision-main/src/rm_auto_aim-main)
- 启动配置与参数：[rm_vision_bringup](./RM-QIQI-vision-main/src/rm_vision-main/rm_vision_bringup)
- 海康相机模块：[ros2_hik_camera-main](./RM-QIQI-vision-main/src/ros2_hik_camera-main)
- 串口通信模块：[rm_serial_driver-main](./RM-QIQI-vision-main/src/rm_serial_driver-main)

> 说明：本项目包含对 RoboMaster 开源视觉生态的学习、部署、集成、调试与文档沉淀。README 中强调的是我的落地工作和团队贡献，原开源项目请参考 [rm_vision](https://github.com/chenjunnn/rm_vision)。

### 2. CubiclePal_MVP_v0：桌面智能助手 MVP

CubiclePal 是一个 Python 桌面智能助手项目，目标是把桌面宠物、任务管理、隐私保护和出行规划组合成一个可运行的办公辅助工具。

**核心功能**

- 桌面宠物窗口和系统托盘：基于 PyQt5 实现宠物显示、拖拽、右键菜单、对话框入口。
- 任务管理：通过自然语言解析任务，写入 SQLite，并提供提醒服务与任务状态管理。
- 隐私保护：基于 OpenCV Haar 人脸检测判断用户是否离座，并触发锁屏保护。
- 出行规划：解析目的地、预算、天数和偏好，生成行程方案，并支持导出 Markdown。
- 工程化结构：`src/ai`、`src/core`、`src/ui`、`src/utils` 分层清晰，配套测试/演示脚本。

**可验证内容**

- 主入口：[main.py](./CubiclePal_MVP_v0/main.py)
- UI 层：[src/ui](./CubiclePal_MVP_v0/src/ui)
- 业务逻辑：[src/core](./CubiclePal_MVP_v0/src/core)
- 数据与配置：[src/utils/database.py](./CubiclePal_MVP_v0/src/utils/database.py)、[resource/config.yaml](./CubiclePal_MVP_v0/resource/config.yaml)
- 测试与演示：[test](./CubiclePal_MVP_v0/test)

### 3. TicketingSystem：景区票务管理系统

TicketingSystem 是一个 Java/Maven 多模块项目，围绕景区票务业务进行建模，包含用户、景点、票种、预约、订单、支付等模块。

**技术与结构**

- `TicketingSystem_main`：Spring Boot Web 主模块，包含 Controller、Service、Mapper、POJO、DTO、配置和前端静态资源。
- `PeriodicTask`：独立定时任务模块。
- 数据访问：MyBatis-Plus + Mapper XML。
- 基础设施：MySQL 驱动、Druid 数据源、Spring Security Core、POI 文件处理。

**可验证内容**

- Maven 多模块配置：[pom.xml](./TicketingSystem/pom.xml)
- 主模块依赖：[TicketingSystem_main/pom.xml](./TicketingSystem/TicketingSystem_main/pom.xml)
- Controller 层：[controller](./TicketingSystem/TicketingSystem_main/src/main/java/com/sdut/controller)
- Service 层：[service](./TicketingSystem/TicketingSystem_main/src/main/java/com/sdut/service)
- Mapper 层：[mapper](./TicketingSystem/TicketingSystem_main/src/main/java/com/sdut/mapper)
- 配置文件：[application.yml](./TicketingSystem/TicketingSystem_main/src/main/resources/application.yml)

### 4. Zork-Qt-RPG：基于 Qt 的 Roguelike RPG 游戏

Zork-Qt-RPG 是一个 C++/Qt 项目，适合展示面向对象设计、GUI 事件处理和游戏状态管理能力。

**核心实现**

- 房间与地图：`Room` 维护相邻房间、道具、怪物和房间描述。
- 角色状态：`Character` 维护生命、耐力、武器值、分数和道具效果。
- 道具系统：`Food`、`Weapon`、`Scholarism` 继承/复用 `Item`，实现不同属性加成。
- 战斗逻辑：`Judge` 处理战斗、逃跑、耐力消耗和胜负判断。
- Qt 界面：`MainWindow`、`monsterRoomDialog`、`gameoverDialog` 实现图形化交互。

**可验证内容**

- Qt 工程文件：[Lab56.pro](./Zork-Qt-RPG/Lab56.pro)
- 游戏逻辑入口：[ZorkUL.cpp](./Zork-Qt-RPG/sourceFile/ZorkUL.cpp)
- 战斗判定：[Judge.cpp](./Zork-Qt-RPG/sourceFile/Judge.cpp)
- UI 交互：[mainwindow.cpp](./Zork-Qt-RPG/sourceFile/mainwindow.cpp)

### 5. SoftwareTest：软件测试工程实践

SoftwareTest 用于展示我对基础测试方法和 JUnit 自动化测试的理解，分为两个阶段：

- `SoftwareTest_1`：对排序、搜索、数学函数等基础算法进行单元测试，覆盖正常输入、边界输入和异常输入。
- `SoftwareTest_2`：围绕 `NextDay` 和 `CubeVolume` 设计更系统的边界值分析、等价类划分和参数化测试。

**可验证内容**

- A1 源码：[src/main/java](./SoftwareTest/SoftwareTest_1/softwareTest_A1code/src/main/java)
- A1 测试：[src/test/java](./SoftwareTest/SoftwareTest_1/softwareTest_A1code/src/test/java)
- A2 源码：[src/main/java](./SoftwareTest/SoftwareTest_2/softwareTest_A2code/src/main/java/qhaooolg/softwareTest_A2code)
- A2 测试：[src/test/java](./SoftwareTest/SoftwareTest_2/softwareTest_A2code/src/test/java/qhaooolg/softwareTest_A2code)
- 测试报告文档：[SoftwareTest_1/softwareTest_A1_report.doc](./SoftwareTest/SoftwareTest_1/softwareTest_A1_report.doc)、[SoftwareTest_2/Report_Assignment 2 Part 2 2024.doc](./SoftwareTest/SoftwareTest_2/Report_Assignment%202%20Part%202%202024.doc)

## 荣誉与经历摘要

- RoboMaster 齐奇战队算法组组长：负责视觉/算法方向研发推进、实车调试与成员培养。
- 第 23 届全国大学生机器人大赛 RoboMaster 超级对抗赛全国赛三等奖，工程机器人组/雷达组相关角色。
- 2024 中国工程机器人大赛暨国际公开赛双足竞步赛目一等奖。
- “建行杯”山东省大学生创新大赛省级金奖，智乒先锋项目核心成员。
- 山东省大学生智能技术应用设计大赛多项奖项，曾承担双足竞步/竞速、舞蹈机器人方向技术负责人角色。
- 学术成果：`UNDERWATER IMAGE ENHANCEMENT TECHNIQUE BASED ON CYCLEGAN AND FREQUENCY DECOMPOSITION CORRECTION MODEL` 论文二作。

## 仓库说明

- 本仓库主要用于求职投递时集中展示项目经历，不是单一产品仓库。
- 部分项目来自课程设计、竞赛部署或开源项目集成实践，因此每个子目录保留了不同阶段的代码、报告、文档和演示材料。
- 对招聘方而言，建议重点关注：我的职责是否清晰、代码结构是否可读、项目文档是否能说明问题、以及经历是否与目标岗位匹配。

