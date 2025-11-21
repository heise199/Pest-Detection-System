from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db  # 保留你的数据库依赖（如果报错可临时注释）

# 复制 password_reset.py 中的核心路由定义
router = APIRouter(prefix="/test", tags=["password"])

@router.get("/health")
async def health_check():
    return {"message": "Test routes are working!", "status": "ok"}

# 新建一个独立的 FastAPI 应用，只注册这个路由
# app = FastAPI()
# app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("test_pwd:app", host="127.0.0.1", port=8001, reload=True)