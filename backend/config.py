from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "pest_detection_db"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Paths
    MODEL_PATH: str = "runs/agropest_yolov8n2/weights/best.pt"
    UPLOAD_DIR: str = "uploads"

    # Email Configuration (单邮箱配置 - 向后兼容)
    SMTP_HOST: str = "smtp.gmail.com"  # 默认使用Gmail，可在.env中修改
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # 发送邮件的邮箱地址
    SMTP_PASSWORD: str = ""  # 邮箱密码或应用专用密码
    SMTP_FROM_EMAIL: str = ""  # 发件人邮箱（通常与SMTP_USER相同）
    SMTP_USE_TLS: bool = True  # 使用TLS（端口587）或SSL（端口465）
    SMTP_USE_SSL: bool = False  # 如果使用SSL（端口465），设置为True
    
    # 多邮箱配置（JSON格式，优先级高于单邮箱配置）
    # 格式示例：'[{"host":"smtp.gmail.com","port":587,"user":"xxx@gmail.com","password":"xxx","from_email":"xxx@gmail.com","use_tls":true,"use_ssl":false,"priority":1}]'
    SMTP_CONFIGS: str = ""  # 多个SMTP配置的JSON字符串，留空则使用单邮箱配置

    class Config:
        env_file = ".env"

settings = Settings()

