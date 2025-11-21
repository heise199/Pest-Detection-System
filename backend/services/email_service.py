"""
邮件发送服务
支持通过SMTP发送验证码邮件
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional
import logging

from backend.config import settings

logger = logging.getLogger(__name__)


def send_verification_email(email: str, code: str) -> bool:
    """
    发送验证码邮件
    
    Args:
        email: 收件人邮箱
        code: 验证码
        
    Returns:
        bool: 发送是否成功
    """
    # 检查邮件配置是否完整
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("邮件配置不完整，无法发送邮件。请在.env文件中配置SMTP_USER和SMTP_PASSWORD")
        return False
    
    try:
        # 创建邮件内容
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
        msg['To'] = email
        msg['Subject'] = Header('密码重置验证码', 'utf-8')
        
        # 邮件正文（HTML格式）
        html_content = f"""
        <html>
          <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #333;">密码重置验证码</h2>
              <p>您好，</p>
              <p>您正在重置账户密码，验证码为：</p>
              <div style="background-color: #f4f4f4; padding: 15px; text-align: center; margin: 20px 0;">
                <h1 style="color: #007bff; font-size: 32px; margin: 0; letter-spacing: 5px;">{code}</h1>
              </div>
              <p>验证码有效期为 <strong>5分钟</strong>，请勿泄露给他人。</p>
              <p>如果这不是您的操作，请忽略此邮件。</p>
              <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
              <p style="color: #999; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
            </div>
          </body>
        </html>
        """
        
        # 纯文本格式（备用）
        text_content = f"""
        密码重置验证码
        
        您好，
        
        您正在重置账户密码，验证码为：{code}
        
        验证码有效期为 5分钟，请勿泄露给他人。
        
        如果这不是您的操作，请忽略此邮件。
        
        此邮件由系统自动发送，请勿回复。
        """
        
        # 添加邮件内容
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 发送邮件
        if settings.SMTP_USE_SSL:
            # 使用SSL连接（端口465）
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # 使用TLS连接（端口587）
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        
        logger.info(f"验证码邮件已成功发送到 {email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP认证失败，请检查邮箱用户名和密码")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"发送邮件时发生错误: {str(e)}")
        return False

