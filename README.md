# 害虫检测系统 (Pest Detection System)

基于 YOLOv8 的智能害虫检测平台，支持图片上传检测、实时视频流检测、用户管理、论坛交流等功能。

## 📋 目录

- [项目介绍](#项目介绍)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [API 文档](#api-文档)
- [测试指南](#测试指南)
- [项目结构](#项目结构)
- [常见问题](#常见问题)
- [开发计划](#开发计划)

## 🎯 项目介绍

本项目是一个前后端分离的害虫检测 Web 应用系统，集成了训练好的 YOLOv8 模型，能够识别 12 种常见农林害虫：

- Ants (蚂蚁)
- Bees (蜜蜂)
- Beetles (甲虫)
- Caterpillars (毛毛虫)
- Earthworms (蚯蚓)
- Earwigs (蠼螋)
- Grasshoppers (蚱蜢)
- Moths (飞蛾)
- Slugs (蛞蝓)
- Snails (蜗牛)
- Wasps (黄蜂)
- Weevils (象鼻虫)

## ✨ 功能特性

### 用户功能
- ✅ **用户注册/登录** - JWT 身份认证
- ✅ **图片检测** - 上传图片进行害虫检测，显示检测结果和标注框
- ✅ **实时视频流检测** - 摄像头实时检测
- ✅ **检测历史** - 查看历史检测记录，支持 PDF 报告下载
- ✅ **个人信息管理** - 查看和编辑个人资料

### 社区功能
- ✅ **论坛发帖** - 发布帖子交流
- ✅ **评论互动** - 对帖子进行评论
- ✅ **点赞功能** - 支持帖子点赞/取消点赞

### 管理功能
- ✅ **害虫百科管理** - 管理员可添加/编辑害虫信息
- ✅ **用户管理** - 查看所有用户信息
- ✅ **数据统计** - 查看系统统计数据

### 额外功能
- ✅ **数据可视化** - ECharts 图表展示检测趋势
- ✅ **PDF 报告生成** - 一键生成检测报告

## 🛠 技术栈

### 后端
- **框架**: FastAPI 0.109.0
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose)
- **AI 模型**: YOLOv8 (Ultralytics)
- **图像处理**: OpenCV
- **PDF 生成**: fpdf2

### 前端
- **框架**: Vue 3
- **构建工具**: Vite 7.2
- **UI 组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **图表库**: ECharts

## 📦 环境要求

### 必需环境
- **Python**: 3.8+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **npm**: 8+ 或 **yarn**

### 推荐环境
- **操作系统**: Windows 10/11, Linux, macOS
- **Python 包管理**: pip
- **数据库工具**: Navicat, MySQL Workbench (可选)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd 9517proj
```

### 2. 数据库配置

#### 方式一：使用 SQL 文件（推荐）

1. 确保 MySQL 服务运行在 `localhost:3306`
2. 使用数据库工具（如 Navicat）导入 `pest_detection_db.sql`
3. 这将自动创建数据库和表结构

#### 方式二：使用 Python 脚本

```bash
python init_db.py
```

这将创建数据库、表结构，并初始化管理员账号：
- **用户名**: `admin`
- **密码**: `admin123`

### 3. 后端配置

#### 安装依赖

```bash
pip install -r backend/requirements.txt
```

#### 配置数据库连接

编辑 `backend/config.py`（如需要）：

```python
DB_USER: str = "root"          # 数据库用户名
DB_PASSWORD: str = "123456"    # 数据库密码
DB_HOST: str = "localhost"     # 数据库主机
DB_PORT: int = 3306            # 数据库端口
DB_NAME: str = "pest_detection_db"  # 数据库名
```

#### 启动后端服务

```bash
# 在项目根目录运行
uvicorn backend.main:app --reload
```

后端服务将在 `http://127.0.0.1:8000` 启动

- **API 文档**: http://127.0.0.1:8000/docs
- **交互式文档**: http://127.0.0.1:8000/redoc

### 4. 前端配置

#### 安装依赖

```bash
cd frontend
npm install
```

#### 启动前端服务

```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 5. 访问应用

打开浏览器访问：**http://localhost:5173**

使用默认管理员账号登录：
- **用户名**: `admin`
- **密码**: `admin123`

## ⚙️ 详细配置

### 后端配置

#### 模型路径配置

确保 `backend/config.py` 中的模型路径正确：

```python
MODEL_PATH: str = "runs/agropest_yolov8n2/weights/best.pt"
```

模型文件应位于项目根目录的 `runs/agropest_yolov8n2/weights/best.pt`

#### 上传目录配置

```python
UPLOAD_DIR: str = "uploads"  # 上传文件保存目录
```

#### JWT 配置

```python
SECRET_KEY: str = "your-super-secret-key-change-me"  # 生产环境请修改
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token 过期时间（分钟）
```

### 前端配置

#### API 代理配置

`frontend/vite.config.js` 中的代理配置：

```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',  // 后端地址
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

#### 环境变量（可选）

创建 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 📚 API 文档

### 认证接口

- `POST /register` - 用户注册
- `POST /token` - 用户登录（获取 JWT Token）

### 用户接口

- `GET /users/me` - 获取当前用户信息

### 检测接口

- `POST /detection/upload` - 上传图片进行检测
- `GET /detection/history` - 获取检测历史
- `GET /detection/video_feed` - 实时视频流检测
- `GET /detection/report/{id}` - 下载检测报告 PDF

### 论坛接口

- `GET /forum/posts` - 获取帖子列表
- `POST /forum/posts` - 创建新帖子
- `POST /forum/posts/{id}/comments` - 添加评论
- `POST /forum/posts/{id}/like` - 点赞/取消点赞

### 管理接口

- `GET /admin/stats` - 获取统计数据（需管理员权限）
- `GET /admin/users` - 获取用户列表（需管理员权限）
- `GET /admin/pests` - 获取害虫列表
- `POST /admin/pests` - 添加害虫信息（需管理员权限）

详细 API 文档请访问：http://127.0.0.1:8000/docs

## 🧪 测试指南

### 功能测试

#### 1. 用户注册登录测试

1. 访问 http://localhost:5173
2. 点击"注册"，创建新账号
3. 使用新账号登录
4. 验证是否能正常进入系统

#### 2. 图片检测测试

1. 登录后进入"检测中心"
2. 选择"图片检测"标签
3. 上传一张包含害虫的图片
4. 验证：
   - 是否显示检测结果
   - 是否显示标注框
   - 是否显示害虫类型和数量

#### 3. 实时视频流测试

1. 进入"检测中心"
2. 选择"实时视频流检测"标签
3. 点击"开启摄像头"
4. 验证是否能正常显示实时检测画面

#### 4. 论坛功能测试

1. 进入"交流论坛"
2. 点击"发布新帖"，创建帖子
3. 验证帖子是否显示
4. 测试评论和点赞功能

#### 5. 检测历史测试

1. 进入"个人中心"
2. 查看"检测历史记录"
3. 点击"下载报告"，验证 PDF 是否正常生成

#### 6. 管理功能测试

1. 使用管理员账号登录
2. 进入"后台管理"
3. 测试：
   - 查看统计数据
   - 查看用户列表
   - 添加害虫信息

### API 测试

#### 使用 Swagger UI

1. 访问 http://127.0.0.1:8000/docs
2. 点击"Authorize"按钮
3. 输入 Token（格式：`Bearer <your-token>`）
4. 测试各个接口

#### 使用 curl

```bash
# 登录获取 Token
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 使用 Token 访问受保护接口
curl -X GET "http://127.0.0.1:8000/users/me" \
  -H "Authorization: Bearer <your-token>"
```

### 连接测试

在浏览器控制台运行 `frontend/test-connection.js` 中的代码，测试前后端连接。

## 📁 项目结构

```
9517proj/
├── backend/                 # 后端代码
│   ├── routers/            # 路由模块
│   │   ├── auth.py        # 认证路由
│   │   ├── users.py       # 用户路由
│   │   ├── detection.py   # 检测路由
│   │   ├── forum.py       # 论坛路由
│   │   └── admin.py       # 管理路由
│   ├── services/          # 服务层
│   │   └── yolo_service.py  # YOLO 模型服务
│   ├── models.py          # 数据库模型
│   ├── schemas.py         # Pydantic 模式
│   ├── database.py        # 数据库配置
│   ├── auth.py           # 认证工具
│   ├── dependencies.py   # 依赖注入
│   ├── config.py         # 配置文件
│   ├── main.py           # 应用入口
│   └── requirements.txt  # Python 依赖
│
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── api/           # API 接口
│   │   │   └── axios.js  # Axios 配置
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── views/         # 页面组件
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── vite.config.js     # Vite 配置
│   └── package.json       # 前端依赖
│
├── runs/                  # 模型文件目录
│   └── agropest_yolov8n2/
│       └── weights/
│           └── best.pt    # YOLOv8 模型权重
│
├── uploads/               # 上传文件目录（自动创建）
├── init_db.py            # 数据库初始化脚本
├── pest_detection_db.sql  # 数据库 SQL 文件
└── README.md             # 本文件
```

## ❓ 常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'backend'`

**解决**: 确保在**项目根目录**运行 `uvicorn backend.main:app --reload`，而不是在 `backend` 目录下。

### 2. 数据库连接失败

**问题**: `OperationalError: (2003, "Can't connect to MySQL server")`

**解决**:
- 确保 MySQL 服务正在运行
- 检查 `backend/config.py` 中的数据库配置
- 确保数据库 `pest_detection_db` 已创建

### 3. 模型文件未找到

**问题**: `FileNotFoundError: [Errno 2] No such file or directory: 'runs/...'`

**解决**: 确保模型文件 `runs/agropest_yolov8n2/weights/best.pt` 存在于项目根目录。

### 4. 前端无法连接后端

**问题**: 前端请求返回 404 或网络错误

**解决**:
- 确保后端服务在 8000 端口运行
- 检查 `frontend/vite.config.js` 中的代理配置
- 查看浏览器控制台的 Network 标签

### 5. 登录后跳转回登录页

**问题**: 登录成功但立即跳转回登录页

**解决**:
- 清除浏览器缓存和 LocalStorage
- 检查浏览器控制台的错误信息
- 确保 Token 正确保存

### 6. 上传图片检测失败

**问题**: 上传后显示"检测失败"

**解决**:
- 检查后端日志，查看具体错误
- 确保模型文件路径正确
- 检查图片格式是否支持（JPG, PNG 等）

### 7. 实时视频流无法显示

**问题**: 点击"开启摄像头"后无画面

**解决**:
- 确保浏览器允许摄像头权限
- 检查是否有其他程序占用摄像头
- 查看后端日志是否有错误

更多问题请参考 `TROUBLESHOOTING.md`

## 🔮 开发计划

### 已完成功能 ✅
- [x] 用户注册/登录系统
- [x] 图片检测功能
- [x] 实时视频流检测
- [x] 检测历史管理
- [x] PDF 报告生成
- [x] 论坛功能（发帖、评论、点赞）
- [x] 管理后台
- [x] 数据可视化

### 计划功能 🚧
- [ ] 视频文件上传检测
- [ ] 批量图片检测
- [ ] 检测结果导出（Excel）
- [ ] 邮件通知功能
- [ ] 移动端适配
- [ ] 多语言支持
- [ ] 检测结果分享功能
- [ ] 害虫识别准确率统计

## 📝 许可证

本项目仅供学习和研究使用。

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件 2086035335@qq.com
  
