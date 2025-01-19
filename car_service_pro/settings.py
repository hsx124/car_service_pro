# Django Allauth 配置
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_PRESERVE_USERNAME_CASING = False

# 密码重置配置
ACCOUNT_PASSWORD_RESET_TIMEOUT_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Car Service Pro] "
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# 认证设置
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 登录设置
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# 站点设置
SITE_ID = 1

# 允许访问的域名
ALLOWED_HOSTS = ['*']  # 开发环境下允许所有主机访问，生产环境请设置具体的域名

# 高德地图API设置
AMAP_KEY = '0522c95d4c6f6c0a3a2c0e8c6e8c6e8c'  # 替换为实际的高德地图 API 密钥

# 邮件密送设置
BCC_EMAILS = [
    'hsx19900829@yahoo.co.jp',  # 客服邮箱
    'adrianne.veasley@hotmail.com',  # 管理层邮箱
]

# 添加邮件相关的其他配置
ADMINS = [
    ('Admin', CONTACT_EMAIL),
]
MANAGERS = ADMINS

# 邮件发送失败时的配置
EMAIL_SUBJECT_PREFIX = '[Car Service Pro] '
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# 会话设置
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = '313300497@qq.com'
EMAIL_HOST_PASSWORD = 'lirziptvjkbjbjfj'
DEFAULT_FROM_EMAIL = 'Car Service Pro <313300497@qq.com>'
CONTACT_EMAIL = '313300497@qq.com'

# CSRF设置
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://3061-240d-1a-117c-1800-7dc7-5071-c18a-8693.ngrok-free.app',
    'http://3061-240d-1a-117c-1800-7dc7-5071-c18a-8693.ngrok-free.app',
]

# Crontab设置
CRONJOBS = [
    ('*/5 * * * *', 'django.core.management.call_command', ['update_booking_status']),
]

# 设置crontab日志文件
CRONTAB_COMMAND_PREFIX = 'PYTHONPATH=/path/to/project'
CRONTAB_COMMAND_SUFFIX = '2>&1'

