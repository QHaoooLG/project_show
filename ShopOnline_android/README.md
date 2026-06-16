# ShopOnline_android

`ShopOnline_android` 是一个基于 Android 原生 Java + SQLite 的本地商品管理 Demo。项目围绕简易电商后台/商品台账场景设计，支持用户注册登录、登录状态保持、商品新增、商品列表、商品编辑删除、关键词搜索、分类筛选和多用户数据隔离，适合作为 Android 基础开发、SQLite 数据持久化和 RecyclerView 交互能力的个人项目展示。

> 当前项目为本地单机应用，不包含远程服务端、真实下单、支付、物流、库存同步等线上商城能力。

## 功能概览

- 用户注册与登录：用户名唯一校验，密码基础校验，登录状态通过 SharedPreferences 保存。
- 密码存储优化：注册时写入 SHA-256 哈希，避免在 SQLite 中保存明文密码。
- 商品管理：维护商品名称、描述、分类、价格、创建时间和所属用户。
- 商品列表：按创建时间倒序展示当前登录用户的商品数据。
- 商品编辑/删除：商品卡片内提供直接操作按钮，替代不稳定的长按上下文菜单。
- 查询筛选：支持按商品名称、描述、分类进行关键词包含搜索，也支持按固定分类筛选。
- 数据隔离：所有商品查询、编辑和删除都带有当前用户 ID 条件，避免不同用户数据混用。
- UI 文案优化：界面统一为商品管理语义，修复原项目中的乱码和损坏 XML。

## 技术栈

| 类型 | 技术 |
| --- | --- |
| 开发语言 | Java |
| UI | Android 原生 View、Material Components、RecyclerView |
| 本地存储 | SQLiteOpenHelper、SharedPreferences |
| 构建工具 | Gradle / Android Gradle Plugin |
| 最低版本 | minSdk 24 |
| 目标版本 | targetSdk 36 |

## 项目结构

```text
ShopOnline_android/
├── app/src/main/java/com/example/shoponline_android/
│   ├── activity/          # 登录、注册页面
│   ├── adapter/           # 商品列表 RecyclerView 适配器
│   ├── data/              # ShopRepository，封装业务访问
│   ├── db/                # SQLiteOpenHelper 与 CRUD
│   ├── fragment/          # 新增商品、商品列表、商品查询
│   ├── model/             # User、Product 数据模型
│   └── utils/             # 登录状态、密码哈希、输入校验工具
├── app/src/main/res/
│   ├── layout/            # Activity、Fragment、商品卡片、编辑弹窗布局
│   ├── menu/              # 退出登录菜单
│   └── values/            # 字符串、颜色、主题资源
├── build.gradle
├── settings.gradle
└── README.md
```

## 核心模块说明

### 用户模块

用户模块由 `LoginActivity`、`RegisterActivity`、`ShopRepository`、`DatabaseHelper` 和 `PrefManager` 组成。

- 注册时校验用户名长度、密码长度和确认密码一致性。
- `ShopRepository.registerUser()` 会对密码执行 SHA-256 哈希后再写入数据库。
- 登录时使用输入密码的哈希值与数据库中的哈希值比对。
- 登录成功后，`PrefManager` 保存用户 ID、用户名和登录状态。

### 商品模块

商品模块由 `AddProductFragment`、`ProductListFragment`、`ProductSearchFragment`、`ProductAdapter`、`Product` 和 `ShopRepository` 组成。

- `AddProductFragment` 负责新增商品，并校验商品名称和价格。
- `ProductListFragment` 展示当前用户全部商品，支持编辑和删除。
- `ProductSearchFragment` 支持全部商品查看、关键词搜索和分类筛选。
- `ProductAdapter` 负责商品卡片展示，列表页显示编辑/删除按钮，查询页以只读方式展示。

## 数据库设计

数据库文件：`shoponline_android.db`

### users 表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 用户 ID |
| `username` | TEXT | UNIQUE NOT NULL | 用户名 |
| `password` | TEXT | NOT NULL | SHA-256 密码哈希 |
| `created_at` | TEXT | NOT NULL | 注册时间 |

### products 表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 商品 ID |
| `user_id` | INTEGER | NOT NULL | 所属用户 ID |
| `name` | TEXT | NOT NULL | 商品名称 |
| `description` | TEXT | 可为空 | 商品描述 |
| `category` | TEXT | NOT NULL | 商品分类 |
| `price` | REAL | NOT NULL | 商品价格 |
| `created_at` | TEXT | NOT NULL | 创建时间 |

`products.user_id` 通过外键关联 `users.id`，并启用外键约束。项目同时为用户名、商品所属用户、商品名称和商品分类建立索引，提升常用查询路径的可读性和性能。

## 分类与查询

当前商品分类固定为：

- 数码产品
- 服饰鞋包
- 日用百货
- 食品饮料

关键词搜索会匹配商品名称、商品描述和商品分类，使用包含匹配逻辑，例如输入“数码”可以找到分类为“数码产品”的商品。

## 运行方式

### 环境要求

- JDK 17 或更高版本。
- Android SDK，并配置 `ANDROID_HOME`，或在本地 `local.properties` 中设置 `sdk.dir`。
- Android Studio 或可用的 Gradle 环境。

### Android Studio

1. 使用 Android Studio 打开项目根目录。
2. 等待 Gradle 同步完成。
3. 连接模拟器或 Android 设备。
4. 运行 `app` 模块。

### 命令行构建

也可以在项目根目录执行命令行构建：

```powershell
.\gradlew.bat clean assembleDebug
```

构建产物通常位于：

```text
app/build/outputs/apk/debug/app-debug.apk
```

如果项目位于 Windows 中文路径下，`gradle.properties` 中已加入 `android.overridePathCheck=true`，用于允许 Android Gradle Plugin 在当前目录结构下继续构建。

## 二次优化内容

- 将旧的通用数据模型统一重构为商品领域模型：`Product`、`ProductAdapter`、`AddProductFragment`、`ProductListFragment`、`ProductSearchFragment`。
- 将 SQLite 主业务表调整为 `products`，新增价格和分类字段。
- 增加 `ShopRepository`，将 Activity/Fragment 与底层数据库访问解耦。
- 增加 `PasswordUtils` 和 `Validators`，补齐密码哈希和输入校验。
- 修复原项目中的中文乱码、损坏 XML 和不稳定的 RecyclerView 上下文菜单交互。
- 更新 UI 文案和商品卡片布局，使项目更贴近商品管理展示场景。

## 后续可扩展方向

- 使用 Room 替换手写 SQLiteOpenHelper，提升迁移和查询维护性。
- 增加商品图片字段和本地图片选择能力。
- 增加排序条件，例如按价格升序、价格降序、创建时间筛选。
- 增加仪表盘统计，例如商品总数、分类占比和价格区间。
- 若需要扩展为真实电商应用，再单独接入远程 API、订单、库存、支付和物流模块。
