# 前后端连接测试指南

## 快速检查清单

### 1. 确认后端服务运行
在项目根目录运行：
```bash
uvicorn backend.main:app --reload
```
应该看到：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. 测试后端 API
在浏览器打开：http://127.0.0.1:8000/docs
应该能看到 Swagger UI 文档页面。

或者直接访问：http://127.0.0.1:8000/
应该返回：`{"message": "Welcome to Pest Detection API"}`

### 3. 确认前端服务运行
在 `frontend` 目录运行：
```bash
npm run dev
```
应该看到：
```
VITE v7.2.2  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### 4. 检查浏览器控制台
打开浏览器开发者工具 (F12)，查看：
- **Console** 标签：是否有错误信息
- **Network** 标签：查看 API 请求是否发送，状态码是什么

### 5. 常见问题排查

#### 问题1：后端未运行
**症状**：前端显示"网络错误"或请求超时
**解决**：确保后端服务在 8000 端口运行

#### 问题2：CORS 错误
**症状**：浏览器控制台显示 CORS 相关错误
**解决**：检查 `backend/main.py` 中的 CORS 配置（应该已经配置为允许所有来源）

#### 问题3：代理配置问题
**症状**：请求 404 或无法连接
**解决**：检查 `frontend/vite.config.js` 中的 proxy 配置

#### 问题4：数据库连接失败
**症状**：后端启动时报数据库连接错误
**解决**：
1. 确保 MySQL 服务运行
2. 确保数据库 `pest_detection_db` 已创建
3. 检查 `backend/config.py` 中的数据库配置

### 6. 测试 API 连接

在浏览器控制台运行以下代码测试连接：

```javascript
// 测试后端根路径
fetch('http://127.0.0.1:8000/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)

// 测试前端代理
fetch('/api/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

如果第一个成功但第二个失败，说明代理配置有问题。
如果两个都失败，说明后端没有运行或端口不对。

