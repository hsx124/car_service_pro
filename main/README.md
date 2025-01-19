# Car Service Pro - 专业用车服务平台

## 项目概述
Car Service Pro 是一个基于Django框架开发的专业用车服务预订平台，为用户提供便捷的车辆预订、司机服务和行程管理功能。平台支持多语言（中文、英语、日语），并提供完整的用户管理和订单处理系统。

## 系统要求
- Python 3.8+
- Django 4.0+
- PostgreSQL 12+
- 其他依赖详见 requirements.txt

## 快速开始

### 1. 环境准备
```bash
# 克隆项目
git clone [项目地址]
cd car_service_pro

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置
```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 创建测试数据（可选）
python manage.py create_test_data
```

### 3. 运行服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看网站

## 主要功能模块

### 1. 用户管理
- 用户注册和登录
- 个人资料管理
- 多语言支持
- 权限控制

### 2. 预订系统
- 在线车辆预订
- 多种车型选择
- 实时价格计算
- 订单状态追踪

### 3. 车辆管理
- 车辆信息管理
- 车辆状态监控
- 车型分类管理

### 4. 司机管理
- 司机资料管理
- 司机评价系统
- 司机排班管理

### 5. 评价系统
- 用户评价功能
- 评分统计分析
- 服务质量监控

## 项目结构
```
car_service_pro/
├── car_service/          # 项目配置目录
├── main/                 # 主应用目录
├── templates/            # 模板文件
├── static/              # 静态文件
├── media/               # 媒体文件
├── locale/              # 国际化文件
├── logs/                # 日志文件
└── venv/                # 虚拟环境
```

## 文档
- [用户使用手册](USER_MANUAL.md)
- [开发维护手册](DEVELOPER_GUIDE.md)
- [API文档](API_DOCS.md)

## 定时任务
项目包含以下定时任务：
- 预订状态自动更新（每5分钟）
- 数据库自动备份（每日）

## 部署
详细的部署说明请参考 [部署文档](DEPLOYMENT.md)

## 贡献
欢迎提交 Pull Request 或创建 Issue。

## 许可证
本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式
- 邮箱：313300497@qq.com
- 电话：400-123-4567 