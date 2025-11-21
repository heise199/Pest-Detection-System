import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径，以便直接运行此文件时能找到 backend 模块
# 获取当前文件所在目录的父目录（项目根目录）
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Database Tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Detection API")

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有HTTP请求"""
    logger.info(f"📥 收到请求: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 响应状态: {response.status_code} for {request.method} {request.url.path}")
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all. In prod, specify Vue app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Pest Detection API"}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"message": "API is working!", "status": "ok", "path": "/health"}

@app.get("/api/health")
async def health_check_api():
    """健康检查端点 - 带/api前缀"""
    return {"message": "API is working!", "status": "ok", "path": "/api/health"}

# Import routers

from backend.routers import auth, detection, forum, users, admin, password_reset, test


# Register routers (register API routes BEFORE static file mounts to avoid conflicts)
try:
    app.include_router(auth.router)
    app.include_router(password_reset.router) 
    app.include_router(test.router)
    app.include_router(users.router)
    app.include_router(detection.router)
    app.include_router(forum.router)
    app.include_router(admin.router)
    print("✅ All routers registered successfully")
except Exception as e:
    print(f"❌ Error registering routers: {e}")
    import traceback
    traceback.print_exc()
    raise

# Mount static files AFTER API routes to ensure API routes are matched first
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 调试：打印所有注册的路由
if __name__ == "__main__":
    print("\n📋 已注册的路由:")
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            methods = ", ".join(route.methods) if route.methods else "N/A"
            print(f"  {methods:15} {route.path}")
    print()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
