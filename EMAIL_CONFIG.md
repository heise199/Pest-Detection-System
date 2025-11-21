# 邮件配置说明

## 问题原因

之前的代码**没有实现真正的邮件发送功能**，验证码只是：
- 打印到控制台
- 在API响应中返回（仅用于测试）

所以您收不到邮件是正常的。

## 解决方案

现在已经实现了真正的邮件发送功能。您需要配置SMTP服务器信息。

## 配置步骤

### 1. 创建 `.env` 文件

在项目根目录（`backend` 目录同级）创建 `.env` 文件，添加以下配置：

```env
# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
```

### 2. 不同邮箱服务商的配置

#### Gmail（推荐用于测试）

1. **启用两步验证**：
   - 访问 https://myaccount.google.com/security
   - 启用"两步验证"

2. **生成应用专用密码**：
   - 访问 https://myaccount.google.com/apppasswords
   - 选择"邮件"和"其他（自定义名称）"
   - 将生成的16位密码用作 `SMTP_PASSWORD`

3. **配置示例**：
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # 应用专用密码（16位，去掉空格）
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
```

#### 163邮箱

```env
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=your-email@163.com
SMTP_PASSWORD=your-password  # 或授权码
SMTP_FROM_EMAIL=your-email@163.com
SMTP_USE_TLS=false  # 163使用SSL，不是TLS
```

#### QQ邮箱

```env
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USER=your-email@qq.com
SMTP_PASSWORD=your-authorization-code  # 需要生成授权码
SMTP_FROM_EMAIL=your-email@qq.com
SMTP_USE_TLS=true
```

#### 企业邮箱（如腾讯企业邮箱）

```env
SMTP_HOST=smtp.exmail.qq.com
SMTP_PORT=587
SMTP_USER=your-email@company.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=your-email@company.com
SMTP_USE_TLS=true
```

### 3. 重启后端服务

配置完成后，重启FastAPI后端服务使配置生效。

## 测试

配置完成后，调用 `/password/send-code` 接口，验证码会真正发送到邮箱。

如果邮件发送失败：
- **开发环境**：验证码仍会在控制台打印，方便测试
- **生产环境**：会返回错误信息，不会泄露验证码

## 注意事项

1. **安全性**：
   - `.env` 文件不要提交到Git
   - 使用应用专用密码，不要使用账户密码
   - 生产环境建议使用环境变量或密钥管理服务

2. **邮件发送限制**：
   - Gmail每日发送限制：500封/天（免费账户）
   - 建议生产环境使用专业的邮件服务（如SendGrid、AWS SES等）

3. **开发测试**：
   - 如果暂时无法配置邮件，开发环境下验证码仍会在控制台打印
   - 查看后端控制台输出即可获取验证码

