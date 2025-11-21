"""
邮件发送服务
支持通过SMTP发送验证码邮件
支持多邮箱配置和自动选择
"""
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional, List, Dict
import logging

from backend.config import settings

logger = logging.getLogger(__name__)


# 邮箱域名到SMTP服务器的映射（用于自动选择最佳SMTP）
EMAIL_DOMAIN_SMTP_MAP = {
    'gmail.com': 'smtp.gmail.com',
    '163.com': 'smtp.163.com',
    '126.com': 'smtp.126.com',
    'qq.com': 'smtp.qq.com',
    'sina.com': 'smtp.sina.com',
    'sina.cn': 'smtp.sina.cn',
    'outlook.com': 'smtp-mail.outlook.com',
    'hotmail.com': 'smtp-mail.outlook.com',
    'live.com': 'smtp-mail.outlook.com',
    'yahoo.com': 'smtp.mail.yahoo.com',
    'foxmail.com': 'smtp.qq.com',
}


def _parse_smtp_configs() -> List[Dict]:
    """
    解析SMTP配置
    优先使用多邮箱配置，如果没有则使用单邮箱配置
    """
    configs = []
    
    # 如果配置了多邮箱（JSON格式）
    if settings.SMTP_CONFIGS and settings.SMTP_CONFIGS.strip():
        try:
            configs = json.loads(settings.SMTP_CONFIGS)
            if not isinstance(configs, list):
                logger.warning("SMTP_CONFIGS 必须是JSON数组格式")
                configs = []
        except json.JSONDecodeError as e:
            logger.error(f"解析SMTP_CONFIGS失败: {e}")
            configs = []
    
    # 如果没有多邮箱配置，使用单邮箱配置
    if not configs and settings.SMTP_USER and settings.SMTP_PASSWORD:
        configs = [{
            'host': settings.SMTP_HOST,
            'port': settings.SMTP_PORT,
            'user': settings.SMTP_USER,
            'password': settings.SMTP_PASSWORD,
            'from_email': settings.SMTP_FROM_EMAIL or settings.SMTP_USER,
            'use_tls': settings.SMTP_USE_TLS,
            'use_ssl': settings.SMTP_USE_SSL,
            'priority': 1
        }]
    
    # 按优先级排序（priority越小优先级越高）
    configs.sort(key=lambda x: x.get('priority', 999))
    
    return configs


def _select_best_smtp(email: str, configs: List[Dict]) -> List[Dict]:
    """
    根据收件人邮箱选择最佳的SMTP配置列表（按优先级排序）
    
    Args:
        email: 收件人邮箱
        configs: SMTP配置列表
        
    Returns:
        排序后的SMTP配置列表（最佳匹配在前）
    """
    if not configs:
        return []
    
    # 提取收件人邮箱域名
    email_domain = email.split('@')[-1].lower() if '@' in email else ''
    
    # 查找匹配的SMTP服务器
    preferred_host = EMAIL_DOMAIN_SMTP_MAP.get(email_domain)
    
    if preferred_host:
        # 将匹配的SMTP配置提前
        matched = [c for c in configs if c.get('host') == preferred_host]
        others = [c for c in configs if c.get('host') != preferred_host]
        return matched + others
    
    # 如果没有匹配，返回原始顺序（已按priority排序）
    return configs


def _create_email_message(to_email: str, code: str, from_email: str) -> MIMEMultipart:
    """
    创建邮件消息
    """
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
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
    
    return msg


def _send_with_smtp(msg: MIMEMultipart, config: Dict) -> bool:
    """
    使用指定的SMTP配置发送邮件
    
    Args:
        msg: 邮件消息对象
        config: SMTP配置字典
        
    Returns:
        bool: 发送是否成功
    """
    host = config.get('host')
    port = config.get('port', 587)
    user = config.get('user')
    password = config.get('password')
    use_tls = config.get('use_tls', True)
    use_ssl = config.get('use_ssl', False)
    
    try:
        if use_ssl:
            # 使用SSL连接（端口465）
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            # 使用TLS连接（端口587）
            with smtplib.SMTP(host, port) as server:
                if use_tls:
                    server.starttls()
                server.login(user, password)
                server.send_message(msg)
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP认证失败 ({host}): {str(e)}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP错误 ({host}): {str(e)}")
        return False
    except Exception as e:
        logger.error(f"发送邮件时发生错误 ({host}): {str(e)}")
        return False


def send_verification_email(email: str, code: str) -> bool:
    """
    发送验证码邮件
    支持多邮箱配置和自动故障转移
    
    Args:
        email: 收件人邮箱
        code: 验证码
        
    Returns:
        bool: 发送是否成功
    """
    # 解析SMTP配置
    configs = _parse_smtp_configs()
    
    if not configs:
        logger.warning("邮件配置不完整，无法发送邮件。请在.env文件中配置SMTP_USER和SMTP_PASSWORD，或配置SMTP_CONFIGS")
        return False
    
    # 根据收件人邮箱选择最佳SMTP配置
    sorted_configs = _select_best_smtp(email, configs)
    
    # 创建邮件消息
    from_email = sorted_configs[0].get('from_email', sorted_configs[0].get('user'))
    msg = _create_email_message(email, code, from_email)
    
    # 尝试发送邮件（如果第一个失败，尝试下一个）
    last_error = None
    for i, config in enumerate(sorted_configs):
        host = config.get('host')
        logger.info(f"尝试使用 SMTP 服务器 {host} 发送邮件到 {email} (尝试 {i+1}/{len(sorted_configs)})")
        
        if _send_with_smtp(msg, config):
            logger.info(f"验证码邮件已成功发送到 {email} (使用 {host})")
            return True
        else:
            last_error = f"SMTP服务器 {host} 发送失败"
            if i < len(sorted_configs) - 1:
                logger.warning(f"{last_error}，尝试下一个SMTP服务器...")
    
    # 所有SMTP服务器都失败了
    logger.error(f"所有SMTP服务器都发送失败，无法发送邮件到 {email}")
    return False
