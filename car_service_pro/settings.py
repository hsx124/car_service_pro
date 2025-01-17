# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 开发环境使用控制台后端
DEFAULT_FROM_EMAIL = 'Car Service Pro <noreply@qq.com>'
CONTACT_EMAIL = '313300497@qq.com'  # 接收联系表单提交的邮箱

# 添加邮件相关的其他配置
ADMINS = [
    ('Admin', CONTACT_EMAIL),
]
MANAGERS = ADMINS

# 邮件发送失败时的配置
EMAIL_SUBJECT_PREFIX = '[Car Service Pro] '
SERVER_EMAIL = DEFAULT_FROM_EMAIL 