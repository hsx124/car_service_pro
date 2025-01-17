# Car Service Pro - 专业用车服务平台

## 项目简介
Car Service Pro 是一个专业的用车服务预订平台，为用户提供便捷的车辆预订、司机服务和行程管理功能。平台支持多语言（中文、日语），并提供完整的用户管理和订单处理系统。

## 主要功能

### 1. 用户功能
- 用户注册和登录
- 个人资料管理（头像、联系方式、地址等）
- 语言偏好设置（中文、日语）
- 通知设置管理

### 2. 预订系统
- 在线车辆预订
- 多种车型选择（经济型、商务型、豪华型）
- 灵活的时间和地点选择
- 特殊需求备注
- 实时价格估算
- 预订确认邮件通知

### 3. 订单管理
- 预订历史查看
- 订单状态跟踪（待确认、已确认、进行中、已完成、已取消）
- 订单取消功能
- 评价和反馈系统

### 4. 车辆和司机
- 多样化车型展示
- 专业司机团队
- 司机评价系统
- 多语言服务支持

### 5. 安全和支持
- 完整的安全保障体系
- 24小时客户服务
- 在线咨询支持
- 常见问题解答

## 技术栈
- 后端：Django
- 数据库：SQLite
- 前端：Bootstrap, JavaScript
- 邮件服务：SMTP
- 多语言支持：Django i18n
- 文件存储：Django Storage

## 安装说明

1. 克隆项目
```bash
git clone [项目地址]
cd car_service_pro
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 数据库迁移
```bash
python manage.py migrate
```

5. 创建测试数据
```bash
python manage.py create_test_data
```

6. 运行开发服务器
```bash
python manage.py runserver
```

## 环境要求
- Python 3.8+
- Django 4.0+
- 其他依赖详见 requirements.txt

## 配置说明

### 邮件配置
在 settings.py 中配置邮件服务：
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your_email@qq.com'
EMAIL_HOST_PASSWORD = 'your_authorization_code'
```

### 定时任务
使用 Windows Task Scheduler 设置以下定时任务：
- 预订状态自动更新：每5分钟执行一次
- 数据库备份：每天凌晨执行

## 使用说明

### 管理员
1. 访问 `/admin` 进入管理后台
2. 管理用户、车辆、司机和预订信息
3. 查看系统日志和统计数据

### 用户
1. 注册/登录账号
2. 完善个人资料
3. 浏览车型和服务
4. 提交预订需求
5. 管理订单和评价

## 联系方式
- 网站：[网站地址]
- 邮箱：[联系邮箱]
- 电话：[联系电话]

## 许可证
[许可证类型] 