# 个人邮箱SMTP发送权限配置指南

本指南将帮助您为不同的个人邮箱服务商配置SMTP发送权限。

## 📧 Gmail（推荐）

### 步骤1：启用两步验证

1. 访问：https://myaccount.google.com/security
2. 找到"登录 Google"部分
3. 点击"两步验证"
4. 按照提示完成设置（需要手机号）

### 步骤2：生成应用专用密码

1. 访问：https://myaccount.google.com/apppasswords
   - 如果看不到此页面，确保已启用两步验证
2. 选择应用：选择"邮件"
3. 选择设备：选择"其他（自定义名称）"
   - 输入名称，如："害虫检测系统"
4. 点击"生成"
5. 会显示一个16位的密码，格式如：`xxxx xxxx xxxx xxxx`
6. **重要**：复制这个密码（去掉空格），这就是您的 `SMTP_PASSWORD`

### 步骤3：配置.env文件

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=你的Gmail地址@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # 应用专用密码（去掉空格）
SMTP_FROM_EMAIL=你的Gmail地址@gmail.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### ⚠️ 注意事项

- **不要使用账户密码**：必须使用应用专用密码
- **每日发送限制**：免费Gmail账户每天最多发送500封邮件
- **安全性**：应用专用密码可以随时撤销，不影响主账户

---

## 📧 163邮箱（网易邮箱）

### 步骤1：开启SMTP服务

1. 登录163邮箱：https://mail.163.com
2. 点击右上角"设置" → "POP3/SMTP/IMAP"
3. 开启"POP3/SMTP服务"和"IMAP/SMTP服务"
4. 可能需要手机验证

### 步骤2：获取授权码

1. 在"POP3/SMTP/IMAP"设置页面
2. 找到"授权码"部分
3. 点击"开启"或"重置授权码"
4. 按照提示获取授权码（通常是16位字符）
5. 这个授权码就是您的 `SMTP_PASSWORD`

### 步骤3：配置.env文件

```env
SMTP_HOST=smtp.163.com
SMTP_PORT=465
SMTP_USER=你的邮箱@163.com
SMTP_PASSWORD=你的授权码  # 不是登录密码！
SMTP_FROM_EMAIL=你的邮箱@163.com
SMTP_USE_TLS=false
SMTP_USE_SSL=true
```

### ⚠️ 注意事项

- **必须使用授权码**：不能使用登录密码
- **端口465**：163邮箱使用SSL，端口是465
- **每日限制**：免费163邮箱每天发送限制约200-500封

---

## 📧 QQ邮箱

### 步骤1：开启SMTP服务

1. 登录QQ邮箱：https://mail.qq.com
2. 点击"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"POP3/SMTP服务"和"IMAP/SMTP服务"

### 步骤2：获取授权码

1. 开启服务后，点击"生成授权码"
2. 按照提示完成验证（可能需要手机验证）
3. 会生成一个授权码（通常是16位字符）
4. 这个授权码就是您的 `SMTP_PASSWORD`

### 步骤3：配置.env文件

```env
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USER=你的QQ号@qq.com
SMTP_PASSWORD=你的授权码  # 不是QQ密码！
SMTP_FROM_EMAIL=你的QQ号@qq.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### ⚠️ 注意事项

- **必须使用授权码**：不能使用QQ密码
- **需要手机验证**：开启服务时需要验证手机号
- **每日限制**：免费QQ邮箱每天发送限制约500封

---

## 📧 126邮箱（网易）

配置方法与163邮箱相同：

```env
SMTP_HOST=smtp.126.com
SMTP_PORT=465
SMTP_USER=你的邮箱@126.com
SMTP_PASSWORD=你的授权码
SMTP_FROM_EMAIL=你的邮箱@126.com
SMTP_USE_TLS=false
SMTP_USE_SSL=true
```

---

## 📧 Outlook/Hotmail

### 步骤1：开启两步验证

1. 访问：https://account.microsoft.com/security
2. 开启"两步验证"

### 步骤2：生成应用密码

1. 访问：https://account.microsoft.com/security
2. 找到"应用密码"
3. 创建新的应用密码
4. 选择"邮件"和"其他"
5. 输入名称，如："害虫检测系统"
6. 复制生成的密码，这就是您的 `SMTP_PASSWORD`

### 步骤3：配置.env文件

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=你的邮箱@outlook.com
SMTP_PASSWORD=你的应用密码
SMTP_FROM_EMAIL=你的邮箱@outlook.com
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

---

## 🔍 快速对比表

| 邮箱服务商 | SMTP服务器 | 端口 | 加密方式 | 需要什么 |
|-----------|-----------|------|---------|---------|
| Gmail | smtp.gmail.com | 587 | TLS | 应用专用密码 |
| 163邮箱 | smtp.163.com | 465 | SSL | 授权码 |
| QQ邮箱 | smtp.qq.com | 587 | TLS | 授权码 |
| 126邮箱 | smtp.126.com | 465 | SSL | 授权码 |
| Outlook | smtp-mail.outlook.com | 587 | TLS | 应用密码 |

---

## ✅ 测试配置

配置完成后，重启后端服务，然后：

1. 调用 `/password/send-code` 接口
2. 查看后端日志，确认是否发送成功
3. 检查收件箱（包括垃圾邮件文件夹）

---

## 🚨 常见问题

### Q1: 为什么Gmail需要应用专用密码？

**A:** Gmail为了安全，不允许直接使用账户密码通过SMTP发送邮件。应用专用密码是专门为第三方应用生成的，可以随时撤销，更安全。

### Q2: 163/QQ邮箱的授权码在哪里找？

**A:** 
- 163邮箱：设置 → POP3/SMTP/IMAP → 授权码
- QQ邮箱：设置 → 账户 → POP3/SMTP服务 → 生成授权码

### Q3: 提示"SMTP认证失败"怎么办？

**A:** 检查以下几点：
1. 确认使用的是**授权码/应用密码**，不是登录密码
2. 确认邮箱地址填写正确（包括@符号）
3. 确认端口和加密方式配置正确
4. 对于Gmail，确认已启用两步验证

### Q4: 邮件发送失败，但配置看起来都对？

**A:** 
1. 检查邮箱的每日发送限制（可能已达到上限）
2. 检查是否被邮箱服务商限制（可能需要验证身份）
3. 查看后端日志的详细错误信息
4. 尝试使用其他邮箱服务商

### Q5: 可以同时配置多个邮箱吗？

**A:** 可以！使用多邮箱配置功能，参考 `MULTI_EMAIL_CONFIG.md`

---

## 💡 推荐配置

### 个人项目/测试环境

**推荐使用Gmail**：
- 配置简单
- 稳定性好
- 每日500封限制通常够用

### 生产环境

**推荐配置2-3个邮箱**：
- 1个Gmail（国际用户）
- 1个163或QQ（国内用户）
- 提高可靠性和发送成功率

---

## 📝 配置检查清单

- [ ] 已获取授权码/应用密码（不是登录密码！）
- [ ] 已正确填写SMTP服务器地址
- [ ] 已正确配置端口号
- [ ] 已正确设置TLS/SSL
- [ ] 已重启后端服务
- [ ] 已测试发送功能

---

## 🔐 安全建议

1. **不要提交.env文件到Git**：已加入.gitignore
2. **定期更换密码**：建议每3-6个月更换一次授权码
3. **限制访问**：只给必要的服务器配置邮箱权限
4. **监控使用**：定期检查邮箱的发送记录，发现异常及时处理

