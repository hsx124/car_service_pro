# Car Service Pro 开发维护手册

## 目录
1. [开发环境配置](#开发环境配置)
2. [项目架构](#项目架构)
3. [代码规范](#代码规范)
4. [数据库设计](#数据库设计)
5. [核心功能模块](#核心功能模块)
6. [国际化支持](#国际化支持)
7. [定时任务](#定时任务)
8. [测试指南](#测试指南)
9. [部署流程](#部署流程)
10. [常见问题](#常见问题)

## 开发环境配置

### 必要软件
- Python 3.8+
- PostgreSQL 12+
- Git
- Visual Studio Code（推荐）

### 开发环境设置
```bash
# 1. 克隆项目
git clone [项目地址]
cd car_service_pro

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 创建本地数据库
createdb car_service_db

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

## 项目架构

### 目录结构说明
```
car_service_pro/
├── car_service/          # 项目配置目录
│   ├── settings.py       # 项目设置
│   ├── urls.py          # URL配置
│   └── wsgi.py          # WSGI配置
├── main/                 # 主应用目录
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图函数
│   ├── urls.py          # URL路由
│   ├── forms.py         # 表单类
│   ├── admin.py         # 管理界面配置
│   └── utils.py         # 工具函数
├── templates/            # HTML模板
├── static/              # 静态文件
└── locale/              # 国际化文件
```

### 核心模块说明
1. **用户认证模块**：使用 django-allauth 实现
2. **预订系统**：自定义实现的预订流程
3. **支付系统**：集成第三方支付接口
4. **评价系统**：自定义实现的评价功能
5. **管理后台**：Django admin 定制化

## 代码规范

### Python代码规范
- 遵循 PEP 8 规范
- 使用4个空格缩进
- 类名使用 CamelCase
- 函数和变量名使用 snake_case
- 添加适当的注释和文档字符串

### 模板代码规范
- 使用2个空格缩进
- 模板标签使用 {% tag %}
- 变量使用 {{ variable }}
- 保持模板结构清晰

### Git提交规范
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式修改
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具的变动
```

## 数据库设计

### 主要模型
1. **User**：用户模型（Django内置）
2. **Vehicle**：车辆信息
3. **Driver**：司机信息
4. **Booking**：预订信息
5. **Review**：评价信息

### 关键字段说明
```python
# 车辆模型示例
class Vehicle(models.Model):
    type = models.CharField(max_length=20)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20)
    # ... 其他字段
```

## 核心功能模块

### 1. 预订流程
1. 用户选择车型
2. 填写预订信息
3. 系统分配司机
4. 确认预订
5. 发送确认邮件

### 2. 状态更新机制
```python
# 预订状态更新示例
def update_booking_status():
    current_time = timezone.now()
    # 更新待确认状态
    Booking.objects.filter(
        status='pending',
        created_at__lte=current_time - timedelta(hours=24)
    ).update(status='cancelled')
```

## 国际化支持

### 翻译文件位置
```
locale/
├── zh_hans/
│   └── LC_MESSAGES/
│       └── django.po
├── en/
│   └── LC_MESSAGES/
│       └── django.po
└── ja/
    └── LC_MESSAGES/
        └── django.po
```

### 翻译步骤
1. 在代码中标记需要翻译的字符串
2. 运行 `django-admin makemessages -l zh_hans`
3. 编辑 .po 文件添加翻译
4. 运行 `django-admin compilemessages`

## 定时任务

### 配置说明
1. 使用 Windows Task Scheduler
2. 设置定时任务运行 update_booking_status.bat
3. 任务频率：每5分钟执行一次

### 关键任务
1. 预订状态更新
2. 数据库备份
3. 邮件通知发送

## 测试指南

### 单元测试
```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test main

# 运行特定测试类
python manage.py test main.tests.TestBooking
```

### 测试覆盖率
```bash
coverage run manage.py test
coverage report
coverage html  # 生成HTML报告
```

## 部署流程

### 准备工作
1. 服务器环境配置
2. 数据库配置
3. 静态文件收集
4. 配置 Nginx 和 uWSGI

### 部署步骤
```bash
# 1. 收集静态文件
python manage.py collectstatic

# 2. 数据库迁移
python manage.py migrate

# 3. 配置 uWSGI
# 4. 配置 Nginx
# 5. 启动服务
```

## 常见问题

### 1. 数据库迁移问题
- 检查迁移文件是否正确
- 使用 `python manage.py showmigrations` 查看状态
- 必要时可以重置迁移

### 2. 静态文件问题
- 确保 STATIC_ROOT 配置正确
- 运行 collectstatic 命令
- 检查 Nginx 配置

### 3. 邮件发送问题
- 检查 SMTP 配置
- 查看邮件发送日志
- 测试邮件服务器连接

## 维护建议

### 日常维护
1. 定期检查日志文件
2. 监控服务器资源使用
3. 定期备份数据库
4. 更新安全补丁

### 性能优化
1. 使用缓存
2. 优化数据库查询
3. 压缩静态文件
4. 使用 CDN

### 安全维护
1. 定期更新依赖包
2. 检查安全漏洞
3. 监控异常访问
4. 维护防火墙规则
``` 