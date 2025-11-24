#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复 .env 文件中的 SMTP_CONFIGS JSON 格式问题
"""
import re

# 读取 .env 文件
with open('.env', 'r', encoding='utf-8') as f:
    content = f.read()

# 正确的SMTP_CONFIGS配置（一行，无换行）
fixed_config = 'SMTP_CONFIGS=[{"host":"smtp.qq.com","port":587,"user":"2086035335@qq.com","password":"VJZRFMFGXFOTRBYG","from_email":"2086035335@qq.com","use_tls":true,"use_ssl":false,"priority":1},{"host":"smtp.163.com","port":465,"user":"yjjy_mfl_1@163.com","password":"YMbzj38SQ8ZkMcvn","from_email":"yjjy_mfl_1@163.com","use_tls":false,"use_ssl":true,"priority":2}]'

# 替换SMTP_CONFIGS配置（匹配多行）
content = re.sub(r'SMTP_CONFIGS=.*', fixed_config, content, flags=re.DOTALL)

# 写回文件
with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ .env 文件已修复！")
print("SMTP_CONFIGS 现在是一行格式，可以正常解析了。")

