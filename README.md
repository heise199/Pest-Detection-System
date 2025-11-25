# 害虫检测系统 - 功能详细说明文档

## 📋 目录

- [系统概述](#系统概述)
- [核心功能模块](#核心功能模块)
  - [1. 用户认证与权限管理](#1-用户认证与权限管理)
  - [2. 害虫检测功能](#2-害虫检测功能)
  - [3. 检测历史管理](#3-检测历史管理)
  - [4. 交流论坛](#4-交流论坛)
  - [5. 害虫百科](#5-害虫百科)
  - [6. 个人中心](#6-个人中心)
  - [7. 后台管理](#7-后台管理)
- [技术实现细节](#技术实现细节)
- [数据模型](#数据模型)
- [API 接口说明](#api-接口说明)
- [使用流程](#使用流程)

---

## 系统概述

本系统是一个基于 YOLOv8 深度学习模型的智能害虫检测平台，采用前后端分离架构，提供完整的用户管理、害虫检测、社区交流和管理功能。系统能够识别 12 种常见农林害虫，支持图片检测、视频检测和实时视频流检测。

### 支持的害虫类型

系统可以识别以下 12 种害虫：

1. **Ants** (蚂蚁)
2. **Bees** (蜜蜂)
3. **Beetles** (甲虫)
4. **Caterpillars** (毛毛虫)
5. **Earthworms** (蚯蚓)
6. **Earwigs** (蠼螋)
7. **Grasshoppers** (蚱蜢)
8. **Moths** (飞蛾)
9. **Slugs** (蛞蝓)
10. **Snails** (蜗牛)
11. **Wasps** (黄蜂)
12. **Weevils** (象鼻虫)

---

## 核心功能模块

### 1. 用户认证与权限管理

#### 1.1 用户注册

**功能描述：**
- 新用户可以通过用户名、邮箱和密码注册账号
- 系统自动验证用户名唯一性和邮箱格式
- 密码采用哈希加密存储，确保安全性

**实现细节：**
- 后端使用 `bcrypt` 进行密码哈希加密
- 前端进行表单验证，确保数据格式正确
- 注册成功后自动跳转到登录页面

**相关文件：**
- 前端：`frontend/src/views/RegisterView.vue`
- 后端：`backend/routers/auth.py`

#### 1.2 用户登录

**功能描述：**
- 支持用户名和密码登录
- 使用 JWT (JSON Web Token) 进行身份认证
- Token 有效期为 30 分钟（可配置）
- 登录成功后保存 Token 到本地存储

**安全特性：**
- Token 存储在浏览器的 LocalStorage 中
- 每次请求自动携带 Token 进行身份验证
- Token 过期后自动跳转到登录页

**相关文件：**
- 前端：`frontend/src/views/LoginView.vue`
- 后端：`backend/routers/auth.py`
- 认证工具：`backend/auth.py`

#### 1.3 密码重置

**功能描述：**
- 用户忘记密码时，可通过邮箱验证码重置密码
- 系统发送 6 位数字验证码到用户邮箱
- 验证码有效期为 5 分钟
- 验证码使用后自动失效

**流程：**
1. 用户输入注册邮箱
2. 系统生成验证码并发送到邮箱
3. 用户输入验证码和新密码
4. 系统验证验证码有效性
5. 验证通过后更新密码

**相关文件：**
- 前端：`frontend/src/views/ForgotPasswordView.vue`
- 后端：`backend/routers/password_reset.py`
- 邮件服务：`backend/services/email_service.py`

#### 1.4 权限管理

**用户角色：**
- **普通用户**：可以访问检测、论坛、个人中心等功能
- **管理员**：拥有所有权限，包括后台管理功能

**权限控制：**
- 前端路由守卫检查用户登录状态和角色
- 后端 API 使用依赖注入验证用户权限
- 未登录用户自动跳转到登录页
- 非管理员用户无法访问管理后台

**相关文件：**
- 路由守卫：`frontend/src/router/index.js`
- 权限依赖：`backend/dependencies.py`

---

### 2. 害虫检测功能

#### 2.1 图片检测

**功能描述：**
- 用户上传图片文件进行害虫检测
- 系统使用 YOLOv8 模型进行实时推理
- 检测结果包含：
  - 标注框（bounding boxes）
  - 害虫类型和数量统计
  - 检测置信度
  - 标注后的图片

**支持格式：**
- JPG/JPEG
- PNG
- 其他常见图片格式

**检测流程：**
1. 用户选择或拖拽图片上传
2. 前端显示上传进度
3. 后端接收图片并保存到 `uploads` 目录
4. YOLO 模型进行推理
5. 生成带标注框的结果图片
6. 统计各类害虫数量
7. 保存检测记录到数据库
8. 返回检测结果给前端显示

**结果展示：**
- 显示原始图片和标注后的图片
- 以列表形式展示检测到的害虫类型和数量
- 支持查看检测详情

**相关文件：**
- 前端：`frontend/src/views/DetectionView.vue`
- 后端：`backend/routers/detection.py`
- YOLO 服务：`backend/services/yolo_service.py`

#### 2.2 视频文件检测

**功能描述：**
- 用户上传视频文件进行批量检测
- 系统对视频进行采样处理（每 30 帧处理一次，提高效率）
- 统计整个视频中检测到的害虫类型和数量

**处理策略：**
- 为提高处理效率，系统每隔 30 帧处理一次
- 统计所有处理帧中检测到的害虫
- 返回整体统计结果

**相关文件：**
- 前端：`frontend/src/views/DetectionView.vue`
- 后端：`backend/routers/detection.py` (upload_video 接口)

#### 2.3 实时视频流检测

**功能描述：**
- 通过摄像头进行实时检测
- 使用 MJPEG 流式传输检测结果
- 实时显示检测框和标签

**技术实现：**
- 使用 OpenCV 捕获摄像头画面
- 对每一帧进行 YOLO 推理
- 使用 Server-Sent Events (SSE) 或 MJPEG 流传输
- 前端通过 `<img>` 标签实时显示

**使用流程：**
1. 用户点击"开启摄像头"按钮
2. 浏览器请求摄像头权限
3. 后端开启视频流端点
4. 前端接收并显示实时检测画面
5. 用户可以随时关闭摄像头

**相关文件：**
- 前端：`frontend/src/views/DetectionView.vue`
- 后端：`backend/routers/detection.py` (video_feed 接口)

---

### 3. 检测历史管理

#### 3.1 历史记录查看

**功能描述：**
- 用户可以查看所有历史检测记录
- 记录按时间倒序排列（最新的在前）
- 显示检测时间、检测类型、检测结果等信息

**记录信息：**
- 检测 ID
- 检测时间
- 检测类型（图片/视频/实时流）
- 检测结果（害虫类型和数量）
- 原始图片/视频路径
- 标注后的图片路径

**相关文件：**
- 前端：`frontend/src/views/ProfileView.vue`
- 后端：`backend/routers/detection.py` (history 接口)

#### 3.2 PDF 报告生成

**功能描述：**
- 用户可以为每次检测生成 PDF 报告
- 报告包含检测详情、统计信息和检测图片
- 支持一键下载

**报告内容：**
- 报告标题和编号
- 检测日期和时间
- 检测到的害虫类型和数量列表
- 标注后的检测图片

**技术实现：**
- 使用 `fpdf2` 库生成 PDF
- 自动嵌入检测图片
- 格式化输出检测结果

**相关文件：**
- 前端：`frontend/src/views/ProfileView.vue`
- 后端：`backend/routers/detection.py` (report 接口)

---

### 4. 交流论坛

#### 4.1 帖子发布

**功能描述：**
- 用户可以发布新帖子
- 帖子包含标题和内容
- 自动记录发布者和发布时间

**功能特性：**
- 标题和内容必填验证
- 发布成功后自动刷新帖子列表
- 支持富文本内容（可扩展）

**相关文件：**
- 前端：`frontend/src/views/ForumView.vue`
- 后端：`backend/routers/forum.py` (create_post 接口)

#### 4.2 帖子浏览

**功能描述：**
- 所有用户都可以浏览论坛帖子
- 帖子按发布时间倒序排列
- 显示帖子标题、内容、作者、发布时间等信息

**展示信息：**
- 帖子标题
- 帖子内容
- 发布者用户名
- 发布时间
- 点赞数量
- 评论数量

**相关文件：**
- 前端：`frontend/src/views/ForumView.vue`
- 后端：`backend/routers/forum.py` (get_posts 接口)

#### 4.3 评论功能

**功能描述：**
- 用户可以对帖子进行评论
- 支持展开/收起评论列表
- 显示评论者、评论内容和评论时间

**交互特性：**
- 点击帖子可展开/收起评论区域
- 评论实时更新到帖子中
- 显示评论者的用户名

**相关文件：**
- 前端：`frontend/src/views/ForumView.vue`
- 后端：`backend/routers/forum.py` (create_comment 接口)

#### 4.4 点赞功能

**功能描述：**
- 用户可以对帖子进行点赞/取消点赞
- 实时更新点赞数量
- 防止重复点赞（同一用户只能点赞一次）

**实现逻辑：**
- 点击点赞按钮切换点赞状态
- 如果已点赞则取消点赞，未点赞则添加点赞
- 前端实时更新点赞数量显示

**相关文件：**
- 前端：`frontend/src/views/ForumView.vue`
- 后端：`backend/routers/forum.py` (like_post 接口)

---

### 5. 害虫百科

#### 5.1 害虫信息浏览

**功能描述：**
- 用户可以浏览所有害虫的详细信息
- 显示害虫名称、描述、防治方法等信息
- 支持害虫图片展示

**信息内容：**
- 害虫名称（中英文）
- 详细描述
- 防治方法
- 害虫图片

**相关文件：**
- 前端：`frontend/src/views/PestInfoView.vue`
- 后端：`backend/routers/admin.py` (get_pests 接口)

#### 5.2 害虫信息管理（管理员）

**功能描述：**
- 管理员可以添加、编辑害虫信息
- 支持上传害虫图片
- 可以设置害虫描述和防治方法

**管理功能：**
- 添加新害虫信息
- 编辑现有害虫信息
- 删除害虫信息（可扩展）

**相关文件：**
- 前端：`frontend/src/views/admin/AdminPestsView.vue`
- 后端：`backend/routers/admin.py` (create_pest_info 接口)

---

### 6. 个人中心

#### 6.1 个人信息查看

**功能描述：**
- 用户查看个人基本信息
- 显示用户名、邮箱、注册时间等信息

**显示信息：**
- 用户名
- 邮箱地址
- 注册时间
- 用户头像（自动生成）

**相关文件：**
- 前端：`frontend/src/views/ProfileView.vue`
- 后端：`backend/routers/users.py`

#### 6.2 个人信息编辑

**功能描述：**
- 用户可以编辑用户名和邮箱
- 支持实时保存
- 表单验证确保数据有效性

**编辑功能：**
- 编辑用户名（必填）
- 编辑邮箱（可选，需验证格式）
- 实时保存更改

**相关文件：**
- 前端：`frontend/src/views/ProfileView.vue`
- 后端：`backend/routers/users.py` (update_profile 接口)

#### 6.3 检测历史

**功能描述：**
- 在个人中心查看所有检测历史
- 支持下载 PDF 报告
- 显示检测统计信息

**相关文件：**
- 前端：`frontend/src/views/ProfileView.vue`
- 后端：`backend/routers/detection.py` (history 接口)

---

### 7. 后台管理

#### 7.1 数据统计

**功能描述：**
- 管理员查看系统整体统计数据
- 包括用户总数、检测总数等信息
- 支持数据可视化展示（可扩展）

**统计信息：**
- 用户总数
- 检测总数
- 各类害虫检测统计（可扩展）

**相关文件：**
- 前端：`frontend/src/views/admin/AdminDashboard.vue`
- 后端：`backend/routers/admin.py` (get_stats 接口)

#### 7.2 用户管理

**功能描述：**
- 管理员查看所有用户列表
- 显示用户基本信息
- 支持用户状态管理（可扩展）

**用户信息：**
- 用户 ID
- 用户名
- 邮箱
- 注册时间
- 是否激活
- 是否管理员

**相关文件：**
- 前端：`frontend/src/views/admin/AdminUsersView.vue`
- 后端：`backend/routers/admin.py` (get_all_users 接口)

#### 7.3 害虫信息管理

**功能描述：**
- 管理员管理害虫百科信息
- 添加、编辑、删除害虫信息
- 上传害虫图片

**相关文件：**
- 前端：`frontend/src/views/admin/AdminPestsView.vue`
- 后端：`backend/routers/admin.py` (pest 相关接口)

#### 7.4 系统管理

**功能描述：**
- 系统配置管理
- 日志查看（可扩展）
- 系统监控（可扩展）

**相关文件：**
- 前端：`frontend/src/views/admin/AdminSystemView.vue`

---

## 技术实现细节

### 后端架构

#### 框架和库
- **FastAPI**：现代、快速的 Web 框架
- **SQLAlchemy**：ORM 数据库操作
- **Pydantic**：数据验证和序列化
- **JWT**：身份认证
- **Ultralytics YOLO**：目标检测模型
- **OpenCV**：图像和视频处理
- **fpdf2**：PDF 生成

#### 项目结构
```
backend/
├── routers/          # 路由模块
│   ├── auth.py      # 认证路由
│   ├── users.py     # 用户路由
│   ├── detection.py # 检测路由
│   ├── forum.py     # 论坛路由
│   ├── admin.py     # 管理路由
│   └── password_reset.py # 密码重置路由
├── services/        # 服务层
│   ├── yolo_service.py    # YOLO 模型服务
│   └── email_service.py   # 邮件服务
├── models.py        # 数据库模型
├── schemas.py       # Pydantic 模式
├── database.py      # 数据库配置
├── auth.py          # 认证工具
├── dependencies.py  # 依赖注入
├── config.py        # 配置文件
└── main.py          # 应用入口
```

#### 核心服务

**YOLO 服务 (`yolo_service.py`)**
- 初始化 YOLOv8 模型
- 图片检测：`predict_image(image_path)`
- 视频帧检测：`predict_video_frame(frame)`
- 返回检测结果和标注图片

**邮件服务 (`email_service.py`)**
- 发送验证码邮件
- 支持多邮箱配置
- 邮件模板管理

### 前端架构

#### 框架和库
- **Vue 3**：渐进式 JavaScript 框架
- **Vite**：快速构建工具
- **Element Plus**：UI 组件库
- **Pinia**：状态管理
- **Vue Router**：路由管理
- **Axios**：HTTP 客户端
- **ECharts**：数据可视化（可扩展）

#### 项目结构
```
frontend/src/
├── api/             # API 接口
│   └── axios.js    # Axios 配置
├── router/         # 路由配置
├── stores/         # Pinia 状态管理
├── views/          # 页面组件
│   ├── admin/      # 管理页面
│   └── ...         # 其他页面
├── layouts/        # 布局组件
├── composables/    # 组合式函数
└── styles/         # 样式文件
```

#### 状态管理

**用户状态 (`stores/user.js`)**
- 用户登录状态
- 用户信息
- Token 管理
- 登录/登出方法

---

## 数据模型

### 用户表 (users)
- `id`：主键
- `username`：用户名（唯一）
- `email`：邮箱（唯一，可选）
- `hashed_password`：加密密码
- `is_active`：是否激活
- `is_admin`：是否管理员
- `created_at`：创建时间

### 检测记录表 (detections)
- `id`：主键
- `user_id`：用户 ID（外键）
- `image_path`：图片路径
- `video_path`：视频路径
- `result_json`：检测结果（JSON）
- `detection_type`：检测类型（image/video/stream）
- `created_at`：创建时间

### 帖子表 (posts)
- `id`：主键
- `title`：标题
- `content`：内容
- `user_id`：作者 ID（外键）
- `created_at`：创建时间

### 评论表 (comments)
- `id`：主键
- `content`：内容
- `post_id`：帖子 ID（外键）
- `user_id`：作者 ID（外键）
- `created_at`：创建时间

### 点赞表 (likes)
- `id`：主键
- `post_id`：帖子 ID（外键）
- `user_id`：用户 ID（外键）

### 害虫信息表 (pest_info)
- `id`：主键
- `name`：害虫名称（唯一）
- `description`：描述
- `control_methods`：防治方法
- `image_url`：图片 URL

### 验证码表 (verification_codes)
- `id`：主键
- `email`：邮箱
- `code`：验证码
- `expires_at`：过期时间
- `used`：是否已使用
- `created_at`：创建时间

---

## API 接口说明

### 认证接口

#### POST /register
用户注册
- **请求体**：`{username, email, password}`
- **响应**：用户信息

#### POST /token
用户登录
- **请求体**：`{username, password}` (form-data)
- **响应**：`{access_token, token_type}`

### 密码重置接口

#### POST /password/send-code
发送验证码
- **请求体**：`{email}`
- **响应**：`{message}`

#### POST /password/verify-code
验证验证码
- **请求体**：`{email, code}`
- **响应**：`{message, verified}`

#### POST /password/reset
重置密码
- **请求体**：`{email, code, new_password}`
- **响应**：`{message}`

### 用户接口

#### GET /users/me
获取当前用户信息
- **需要认证**：是
- **响应**：用户信息

#### PUT /users/me
更新用户信息
- **需要认证**：是
- **请求体**：`{username?, email?}`
- **响应**：更新后的用户信息

### 检测接口

#### POST /detection/upload
上传图片检测
- **需要认证**：是
- **请求**：multipart/form-data (file)
- **响应**：检测结果

#### POST /detection/upload_video
上传视频检测
- **需要认证**：是
- **请求**：multipart/form-data (file)
- **响应**：检测结果

#### GET /detection/video_feed
实时视频流
- **响应**：MJPEG 流

#### GET /detection/history
获取检测历史
- **需要认证**：是
- **查询参数**：`skip`, `limit`
- **响应**：检测记录列表

#### GET /detection/report/{detection_id}
生成 PDF 报告
- **需要认证**：是
- **响应**：PDF 文件

### 论坛接口

#### GET /forum/posts
获取帖子列表
- **查询参数**：`skip`, `limit`
- **响应**：帖子列表

#### POST /forum/posts
创建帖子
- **需要认证**：是
- **请求体**：`{title, content}`
- **响应**：帖子信息

#### POST /forum/posts/{post_id}/comments
添加评论
- **需要认证**：是
- **请求体**：`{content}`
- **响应**：评论信息

#### POST /forum/posts/{post_id}/like
点赞/取消点赞
- **需要认证**：是
- **响应**：`{message: "Liked" | "Unliked"}`

### 管理接口

#### GET /admin/stats
获取统计数据
- **需要认证**：是（管理员）
- **响应**：统计数据

#### GET /admin/users
获取用户列表
- **需要认证**：是（管理员）
- **响应**：用户列表

#### GET /admin/pests
获取害虫列表
- **响应**：害虫列表

#### POST /admin/pests
添加害虫信息
- **需要认证**：是（管理员）
- **请求体**：`{name, description, control_methods, image_url}`
- **响应**：害虫信息

---

## 使用流程

### 新用户注册流程

1. 访问系统首页
2. 点击"注册"按钮
3. 填写用户名、邮箱和密码
4. 提交注册表单
5. 系统验证并创建账号
6. 自动跳转到登录页面
7. 使用新账号登录

### 检测流程

#### 图片检测流程
1. 登录系统
2. 进入"检测中心"
3. 选择"图片检测"标签
4. 点击上传区域或拖拽图片
5. 等待检测完成
6. 查看检测结果和标注图片
7. 系统自动保存检测记录

#### 实时检测流程
1. 登录系统
2. 进入"检测中心"
3. 选择"实时检测"标签
4. 点击"开启摄像头"
5. 允许浏览器访问摄像头
6. 查看实时检测画面
7. 点击"关闭摄像头"结束检测

### 论坛使用流程

1. 登录系统
2. 进入"交流论坛"
3. 浏览帖子列表
4. 点击帖子查看详情和评论
5. 可以发布新帖子
6. 可以对帖子进行评论和点赞

### 查看检测历史流程

1. 登录系统
2. 进入"个人中心"
3. 查看"检测历史记录"部分
4. 浏览历史检测记录
5. 点击"下载报告"生成 PDF

### 密码重置流程

1. 在登录页面点击"忘记密码"
2. 输入注册邮箱
3. 系统发送验证码到邮箱
4. 输入收到的验证码
5. 输入新密码
6. 提交重置请求
7. 使用新密码登录

### 管理员操作流程

1. 使用管理员账号登录
2. 进入"后台管理"
3. 查看系统统计数据
4. 管理用户列表
5. 添加/编辑害虫信息
6. 进行系统配置

---

## 注意事项

### 安全建议

1. **生产环境配置**
   - 修改默认的 JWT Secret Key
   - 使用强密码策略
   - 启用 HTTPS
   - 配置 CORS 白名单

2. **数据库安全**
   - 使用强密码
   - 限制数据库访问 IP
   - 定期备份数据

3. **文件上传安全**
   - 限制文件大小
   - 验证文件类型
   - 扫描恶意文件

### 性能优化

1. **模型加载**
   - YOLO 模型在服务启动时加载，避免重复加载
   - 考虑使用模型缓存

2. **数据库查询**
   - 使用索引优化查询
   - 分页加载大量数据
   - 使用连接池

3. **文件存储**
   - 定期清理旧文件
   - 使用对象存储服务（如 OSS）

### 扩展建议

1. **功能扩展**
   - 批量图片检测
   - 检测结果导出 Excel
   - 邮件通知功能
   - 移动端适配
   - 多语言支持

2. **性能扩展**
   - 使用 Redis 缓存
   - 异步任务队列（Celery）
   - CDN 加速静态资源

3. **监控和日志**
   - 添加日志系统
   - 性能监控
   - 错误追踪

---

## 总结

本系统提供了完整的害虫检测解决方案，包括用户管理、多种检测方式、社区交流和后台管理等功能。系统采用现代化的技术栈，具有良好的可扩展性和维护性。通过详细的文档和清晰的代码结构，便于后续的功能扩展和优化。
