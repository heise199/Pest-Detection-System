# 多邮箱配置说明

## 功能特性

现在系统支持**多邮箱配置**，具有以下特性：

1. **自动选择最佳SMTP服务器**：根据收件人邮箱域名自动选择匹配的SMTP服务器
2. **故障转移**：如果第一个SMTP服务器失败，自动尝试下一个
3. **向后兼容**：如果只配置单邮箱，仍然可以正常使用

## 配置方式

### 方式一：单邮箱配置（简单，向后兼容）

在 `.env` 文件中配置：

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### 方式二：多邮箱配置（推荐，支持故障转移）

在 `.env` 文件中配置 `SMTP_CONFIGS`（JSON格式）：

```env
SMTP_CONFIGS=[{"host":"smtp.gmail.com","port":587,"user":"your-email@gmail.com","password":"your-app-password","from_email":"your-email@gmail.com","use_tls":true,"use_ssl":false,"priority":1},{"host":"smtp.163.com","port":465,"user":"your-email@163.com","password":"your-password","from_email":"your-email@163.com","use_tls":false,"use_ssl":true,"priority":2}]
```

**重要**：JSON字符串必须是一行，不能有换行符！

## 配置参数说明

每个SMTP配置对象包含以下字段：

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `host` | string | SMTP服务器地址 | ✅ |
| `port` | number | SMTP端口（587或465） | ✅ |
| `user` | string | 邮箱账号 | ✅ |
| `password` | string | 邮箱密码或应用专用密码 | ✅ |
| `from_email` | string | 发件人邮箱（通常与user相同） | ✅ |
| `use_tls` | boolean | 是否使用TLS（端口587时true） | ✅ |
| `use_ssl` | boolean | 是否使用SSL（端口465时true） | ✅ |
| `priority` | number | 优先级（数字越小优先级越高） | ❌ 默认999 |

## 完整配置示例

### 示例1：Gmail + 163邮箱

```env
SMTP_CONFIGS=[{"host":"smtp.gmail.com","port":587,"user":"sender@gmail.com","password":"xxxx xxxx xxxx xxxx","from_email":"sender@gmail.com","use_tls":true,"use_ssl":false,"priority":1},{"host":"smtp.163.com","port":465,"user":"sender@163.com","password":"your-password","from_email":"sender@163.com","use_tls":false,"use_ssl":true,"priority":2}]
```

### 示例2：Gmail + QQ邮箱

```env
SMTP_CONFIGS=[{"host":"smtp.gmail.com","port":587,"user":"sender@gmail.com","password":"xxxx xxxx xxxx xxxx","from_email":"sender@gmail.com","use_tls":true,"use_ssl":false,"priority":1},{"host":"smtp.qq.com","port":587,"user":"sender@qq.com","password":"your-authorization-code","from_email":"sender@qq.com","use_tls":true,"use_ssl":false,"priority":2}]
```

### 示例3：三个邮箱（Gmail、163、QQ）

```env
SMTP_CONFIGS=[{"host":"smtp.gmail.com","port":587,"user":"sender1@gmail.com","password":"app-password-1","from_email":"sender1@gmail.com","use_tls":true,"use_ssl":false,"priority":1},{"host":"smtp.163.com","port":465,"user":"sender2@163.com","password":"password-2","from_email":"sender2@163.com","use_tls":false,"use_ssl":true,"priority":2},{"host":"smtp.qq.com","port":587,"user":"sender3@qq.com","password":"auth-code-3","from_email":"sender3@qq.com","use_tls":true,"use_ssl":false,"priority":3}]
```

## 工作原理

### 1. 自动选择SMTP服务器

系统会根据收件人邮箱域名自动选择最佳SMTP服务器：

- 收件人是 `xxx@gmail.com` → 优先使用 `smtp.gmail.com`
- 收件人是 `xxx@163.com` → 优先使用 `smtp.163.com`
- 收件人是 `xxx@qq.com` → 优先使用 `smtp.qq.com`
- 如果没有匹配 → 按优先级顺序使用

### 2. 故障转移

如果第一个SMTP服务器发送失败，系统会自动尝试下一个：

1. 尝试优先级最高的SMTP服务器
2. 如果失败，尝试下一个
3. 直到成功或所有服务器都失败

### 3. 优先级排序

- `priority` 值越小，优先级越高
- 如果没有设置 `priority`，默认为 999（最低优先级）
- 相同优先级的按配置顺序

## 支持的邮箱服务商

系统内置了以下邮箱域名的自动匹配：

| 邮箱域名 | SMTP服务器 |
|---------|-----------|
| gmail.com | smtp.gmail.com |
| 163.com | smtp.163.com |
| 126.com | smtp.126.com |
| qq.com | smtp.qq.com |
| foxmail.com | smtp.qq.com |
| sina.com | smtp.sina.com |
| sina.cn | smtp.sina.cn |
| outlook.com | smtp-mail.outlook.com |
| hotmail.com | smtp-mail.outlook.com |
| live.com | smtp-mail.outlook.com |
| yahoo.com | smtp.mail.yahoo.com |

## 使用建议

1. **生产环境**：配置2-3个邮箱账号，提高可靠性
2. **优先级设置**：
   - 最稳定的邮箱设置为 `priority: 1`
   - 备用邮箱设置为 `priority: 2, 3...`
3. **邮箱选择**：
   - 如果主要用户是Gmail，优先配置Gmail
   - 如果主要用户是163，优先配置163
   - 建议至少配置一个国际邮箱（Gmail）和一个国内邮箱（163/QQ）

## 注意事项

1. **JSON格式**：`SMTP_CONFIGS` 必须是有效的JSON数组，且不能有换行
2. **密码安全**：不要在代码中硬编码密码，使用 `.env` 文件（已加入 `.gitignore`）
3. **Gmail应用专用密码**：Gmail需要使用应用专用密码，不是账户密码
4. **测试**：配置完成后，建议先测试发送，确保所有SMTP服务器都正常工作

## 故障排查

如果邮件发送失败，查看后端日志：

- 会显示尝试了哪些SMTP服务器
- 每个服务器的错误信息
- 最终是否成功发送

日志示例：
```
INFO: 尝试使用 SMTP 服务器 smtp.gmail.com 发送邮件到 user@gmail.com (尝试 1/2)
ERROR: SMTP认证失败 (smtp.gmail.com): ...
WARNING: SMTP服务器 smtp.gmail.com 发送失败，尝试下一个SMTP服务器...
INFO: 尝试使用 SMTP 服务器 smtp.163.com 发送邮件到 user@gmail.com (尝试 2/2)
INFO: 验证码邮件已成功发送到 user@gmail.com (使用 smtp.163.com)
```

