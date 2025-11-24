from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string
from typing import Optional

from backend.database import get_db
from backend.models import User, VerificationCode
from backend.auth import get_password_hash
from backend.services.email_service import send_verification_email
def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

from pydantic import BaseModel

class SendCodeRequest(BaseModel):
    email: str

class VerifyCodeRequest(BaseModel):
    email: str
    code: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str
router = APIRouter(prefix="/password", tags=["password"])

# In-memory storage for verification codes (in production, use Redis)
# For demo, we'll use database


@router.post("/send-code")
async def send_verification_code(request: SendCodeRequest, db: Session = Depends(get_db)):
    email = request.email
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该邮箱未注册"
        )
    
    # Generate verification code
    code = generate_code()
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Save code to database
    verification_code = VerificationCode(
        email=email,
        code=code,
        expires_at=expires_at
    )
    db.add(verification_code)
    db.commit()
    
    # 发送验证码邮件
    email_sent = send_verification_email(email, code)
    
    if not email_sent:
        # 如果邮件发送失败，在开发环境中仍然返回验证码（方便测试）
        # 生产环境中应该记录错误并返回通用消息
        import os
        if os.getenv("ENVIRONMENT", "development") == "development":
            print(f"⚠️ 邮件发送失败，验证码为: {code}")  # 仅开发环境
            return {
                "message": "验证码已发送到邮箱（开发模式：邮件发送失败，请查看控制台）",
                "code": code  # 仅开发环境返回
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="邮件发送失败，请稍后重试或联系管理员"
            )
    
    return {
        "message": "验证码已发送到邮箱，请查收"
    }

@router.post("/verify-code")
async def verify_code(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db)
):
    email = request.email
    code = request.code
    # Find valid code
    verification = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code,
        VerificationCode.used == False,
        VerificationCode.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码无效或已过期"
        )
    
    # 不在这里标记为used，等重置密码成功后再标记
    # 这样验证码可以在验证和重置之间重复使用
    # verification.used = True
    # db.commit()
    
    return {"message": "验证码验证成功", "verified": True}

@router.post("/reset")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    email = request.email
    code = request.code
    new_password = request.new_password
    
    # Verify code first (允许使用已验证但未标记为used的验证码)
    verification = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code,
        VerificationCode.used == False,
        VerificationCode.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码无效或已过期"
        )
    
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    # 密码重置成功后，标记验证码为已使用
    verification.used = True
    db.commit()
    
    return {"message": "密码重置成功"}


@router.get("/health")
async def health_check():
    return {"message": "Password reset routes are working!", "status": "ok"}
