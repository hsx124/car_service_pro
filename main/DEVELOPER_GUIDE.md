# Car Service Pro 开发维护手册

## 目录
1. [开发环境配置](#开发环境配置)
2. [项目架构](#项目架构)
3. [核心模块详解](#核心模块详解)
4. [数据模型说明](#数据模型说明)
5. [视图函数详解](#视图函数详解)
6. [工具函数说明](#工具函数说明)
7. [国际化实现](#国际化实现)
8. [定时任务实现](#定时任务实现)
9. [测试用例说明](#测试用例说明)
10. [部署指南](#部署指南)

## 开发环境配置

### 系统要求
- 操作系统：Windows 10/11, Linux, macOS
- Python 3.8+
- PostgreSQL 12+
- Git
- Visual Studio Code（推荐）

### 依赖包说明
```python
# requirements.txt 核心依赖说明
Django>=4.0.0          # Web框架
django-allauth>=0.54.0 # 用户认证系统
Pillow>=10.0.0        # 图片处理
python-dotenv>=1.0.0   # 环境变量管理
django-crontab>=0.7.1  # 定时任务
```

### 开发环境设置
```bash
# 详细的环境设置步骤
git clone [项目地址]
cd car_service_pro
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## 项目架构

### 目录结构详解
```
car_service_pro/
├── car_service/          # 项目配置目录
│   ├── settings.py       # 核心配置文件
│   ├── urls.py          # 主URL配置
│   └── wsgi.py          # WSGI服务器配置
├── main/                 # 主应用目录
│   ├── models.py        # 数据模型定义
│   ├── views.py         # 视图函数
│   ├── urls.py          # URL路由配置
│   ├── forms.py         # 表单类定义
│   ├── admin.py         # 管理界面配置
│   ├── utils.py         # 工具函数
│   └── templatetags/    # 自定义模板标签
├── templates/           # HTML模板目录
│   ├── base.html       # 基础模板
│   └── main/           # 应用模板
├── static/             # 静态文件
│   ├── css/           # 样式文件
│   ├── js/            # JavaScript文件
│   └── img/           # 图片资源
└── locale/            # 国际化文件
```

## 核心模块详解

### 1. 用户认证模块
```python
# settings.py 认证配置
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 邮箱验证设置
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
```

### 2. 预订系统实现
```python
# views.py 预订处理
def booking(request):
    """
    处理预订请求的主视图函数
    
    流程：
    1. 验证用户登录状态
    2. 处理POST请求：创建新预订
    3. 处理GET请求：显示预订表单
    4. 发送确认邮件
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            send_booking_confirmation_email(booking)
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'main/booking.html', {'form': form})
```

### 3. 价格计算系统
```python
# utils.py 价格计算
def calculate_price(vehicle_type, distance, duration, is_night=False, is_holiday=False):
    """
    计算行程价格
    
    参数：
    - vehicle_type: 车型（经济型/商务型/豪华型）
    - distance: 行程距离（公里）
    - duration: 预计时长（分钟）
    - is_night: 是否夜间服务
    - is_holiday: 是否节假日
    
    返回：
    - total_price: 总价格
    """
    base_price = get_base_price(vehicle_type)
    distance_fee = calculate_distance_fee(distance, vehicle_type)
    time_fee = calculate_time_fee(duration)
    
    total = base_price + distance_fee + time_fee
    
    if is_night:
        total *= 1.2  # 夜间服务费率
    if is_holiday:
        total *= 1.5  # 节假日费率
        
    return total
```

## 数据模型说明

### 1. Vehicle（车辆）模型
```python
class Vehicle(models.Model):
    """
    车辆信息模型
    
    字段说明：
    - type: 车型（经济型/商务型/豪华型）
    - brand: 品牌
    - model: 型号
    - plate_number: 车牌号
    - seats: 座位数
    - status: 车辆状态
    """
    TYPE_CHOICES = [
        ('economy', '经济型'),
        ('business', '商务型'),
        ('luxury', '豪华型'),
    ]
    
    type = models.CharField('车型', max_length=20, choices=TYPE_CHOICES)
    brand = models.CharField('品牌', max_length=50)
    model = models.CharField('型号', max_length=50)
    plate_number = models.CharField('车牌号', max_length=20, unique=True)
    seats = models.IntegerField('座位数')
    status = models.CharField('状态', max_length=20)
```

### 2. Driver（司机）模型
```python
class Driver(models.Model):
    """
    司机信息模型
    
    字段说明：
    - user: 关联的用户账号
    - license_number: 驾驶证号
    - experience_years: 驾龄
    - rating: 评分
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField('驾驶证号', max_length=50)
    experience_years = models.IntegerField('驾龄')
    rating = models.DecimalField('评分', max_digits=3, decimal_places=2)
```

### 3. Booking（预订）模型
```python
class Booking(models.Model):
    """
    预订信息模型
    
    字段说明：
    - user: 预订用户
    - vehicle: 预订车辆
    - driver: 分配司机
    - status: 预订状态
    - price: 价格
    """
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
```

## 视图函数详解

### 1. 首页视图
```python
def home(request):
    """
    首页视图
    
    功能：
    1. 展示可用车辆
    2. 显示热门司机
    3. 展示用户评价
    """
    vehicles = Vehicle.objects.filter(status='available')
    top_drivers = Driver.objects.filter(is_available=True).order_by('-rating')[:3]
    recent_reviews = Review.objects.order_by('-created_at')[:5]
    
    return render(request, 'main/home.html', {
        'vehicles': vehicles,
        'top_drivers': top_drivers,
        'recent_reviews': recent_reviews,
    })
```

### 2. 预订处理视图
```python
@login_required
def booking(request):
    """
    预订处理视图
    
    功能：
    1. 处理预订表单提交
    2. 计算价格
    3. 分配司机
    4. 发送确认邮件
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.price = calculate_price(
                booking.vehicle.type,
                booking.distance,
                booking.duration
            )
            booking.driver = assign_driver(booking)
            booking.save()
            
            send_booking_confirmation_email(booking)
            return redirect('booking_success')
    else:
        form = BookingForm()
    
    return render(request, 'main/booking.html', {'form': form})
```

## 工具函数说明

### 1. 邮件发送
```python
def send_booking_confirmation_email(booking):
    """
    发送预订确认邮件
    
    参数：
    - booking: 预订对象
    
    功能：
    1. 生成邮件内容
    2. 发送确认邮件
    3. 记录发送日志
    """
    subject = f'预订确认 #{booking.id}'
    message = render_to_string('emails/booking_confirmation.html', {
        'booking': booking
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email]
    )
```

### 2. 司机分配
```python
def assign_driver(booking):
    """
    智能分配司机
    
    参数：
    - booking: 预订对象
    
    返回：
    - driver: 分配的司机对象
    
    逻辑：
    1. 检查可用司机
    2. 根据评分和距离计算优先级
    3. 选择最适合的司机
    """
    available_drivers = Driver.objects.filter(
        is_available=True,
        preferred_vehicle_types__contains=booking.vehicle.type
    )
    
    # 计算每个司机的得分
    driver_scores = []
    for driver in available_drivers:
        score = calculate_driver_score(driver, booking)
        driver_scores.append((driver, score))
    
    # 选择得分最高的司机
    if driver_scores:
        return max(driver_scores, key=lambda x: x[1])[0]
    return None
```

## 国际化实现

### 1. 配置说明
```python
# settings.py
LANGUAGES = [
    ('zh-hans', '简体中文'),
    ('en', 'English'),
    ('ja', '日本語'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

### 2. 翻译函数使用
```python
# 在Python代码中
from django.utils.translation import gettext as _

message = _('预订成功')

# 在模板中
{% load i18n %}
{% trans "预订成功" %}
```

## 定时任务实现

### 1. 预订状态更新
```python
def update_booking_status():
    """
    自动更新预订状态
    
    功能：
    1. 更新超时未确认的预订
    2. 更新已完成的行程
    3. 发送相关通知
    """
    current_time = timezone.now()
    
    # 更新超时未确认的预订
    Booking.objects.filter(
        status='pending',
        created_at__lte=current_time - timedelta(hours=24)
    ).update(status='cancelled')
    
    # 更新已完成的行程
    completed_bookings = Booking.objects.filter(
        status='confirmed',
        pickup_time__lte=current_time - timedelta(hours=2)
    )
    for booking in completed_bookings:
        booking.status = 'completed'
        booking.save()
        send_completion_notification(booking)
```

## 测试用例说明

### 1. 模型测试
```python
class VehicleTests(TestCase):
    """车辆模型测试"""
    
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            type='economy',
            brand='丰田',
            model='卡罗拉',
            plate_number='京A12345'
        )
    
    def test_vehicle_creation(self):
        self.assertTrue(isinstance(self.vehicle, Vehicle))
        self.assertEqual(self.vehicle.__str__(), '丰田 卡罗拉')
```

### 2. 视图测试
```python
class BookingViewTests(TestCase):
    """预订视图测试"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_booking_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/booking.html')
```

## 部署指南

### 1. 服务器配置
```bash
# 安装必要软件
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# 创建项目目录
mkdir /var/www/car_service_pro
cd /var/www/car_service_pro

# 克隆项目并设置环境
git clone [项目地址]
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Nginx配置
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/car_service_pro;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### 3. 数据库配置
```sql
CREATE DATABASE car_service_db;
CREATE USER car_service_user WITH PASSWORD 'your_password';
ALTER ROLE car_service_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE car_service_db TO car_service_user;
```

## 维护建议

### 1. 日常维护
- 定期检查日志文件
- 监控服务器资源使用
- 数据库备份
- 更新安全补丁

### 2. 性能优化
- 使用缓存
- 优化数据库查询
- 压缩静态文件
- 使用CDN

### 3. 安全维护
- 定期更新依赖包
- 检查安全漏洞
- 监控异常访问
- 维护防火墙规则

## 系统流程说明

### 1. 请求处理流程
```
浏览器请求 -> Nginx -> uwsgi -> Django URLs -> 视图函数 -> 数据库操作 -> 返回响应
```

#### 详细步骤说明：
1. **URL路由解析**：
```python
# urls.py
urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('api/check-availability/', views.check_availability, name='check-availability'),
]
```

2. **视图函数处理**：
```python
# views.py
def booking(request):
    """
    预订流程示例：
    1. 用户提交表单
    2. 验证表单数据
    3. 检查车辆可用性
    4. 创建预订记录
    5. 发送确认邮件
    """
    if request.method == 'POST':
        # 1. 获取表单数据
        form = BookingForm(request.POST)
        
        # 2. 验证数据
        if form.is_valid():
            # 3. 检查车辆可用性
            vehicle = form.cleaned_data['vehicle']
            if check_vehicle_availability(vehicle, form.cleaned_data['pickup_time']):
                # 4. 创建预订
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                
                # 5. 发送确认邮件
                send_booking_confirmation(booking)
                
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': '车辆不可用'})
    return render(request, 'booking.html', {'form': form})
```

### 2. 数据库交互流程

#### 查询操作示例：
```python
# 1. 基本查询
vehicles = Vehicle.objects.filter(status='available')

# 2. 关联查询
bookings = Booking.objects.select_related('vehicle', 'driver').filter(user=request.user)

# 3. 聚合查询
from django.db.models import Avg, Count
driver_stats = Driver.objects.annotate(
    booking_count=Count('booking'),
    avg_rating=Avg('rating')
).filter(is_active=True)
```

#### 更新操作示例：
```python
# 1. 单条记录更新
booking = Booking.objects.get(id=booking_id)
booking.status = 'confirmed'
booking.save()

# 2. 批量更新
Vehicle.objects.filter(type='economy').update(base_price=200)

# 3. 事务处理
from django.db import transaction

@transaction.atomic
def complete_booking(booking_id):
    booking = Booking.objects.select_for_update().get(id=booking_id)
    booking.status = 'completed'
    booking.save()
    
    # 更新司机状态
    driver = booking.driver
    driver.available = True
    driver.save()
    
    # 创建支付记录
    Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        status='pending'
    )
```

### 3. 前端交互流程

#### AJAX请求处理：
```javascript
// 检查车辆可用性
function checkVehicleAvailability(vehicleId, date) {
    $.ajax({
        url: '/api/check-availability/',
        method: 'POST',
        data: {
            vehicle_id: vehicleId,
            date: date
        },
        success: function(response) {
            if (response.available) {
                showBookingForm();
            } else {
                showErrorMessage('车辆在该时间段不可用');
            }
        }
    });
}

// 提交预订表单
function submitBooking(formData) {
    $.ajax({
        url: '/booking/create/',
        method: 'POST',
        data: formData,
        success: function(response) {
            if (response.status === 'success') {
                showConfirmation(response.booking_id);
            } else {
                showErrorMessage(response.message);
            }
        }
    });
}
```

#### 后端处理AJAX请求：
```python
# views.py
def check_availability(request):
    """
    检查车辆可用性的API端点
    """
    vehicle_id = request.POST.get('vehicle_id')
    date = request.POST.get('date')
    
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        is_available = vehicle.check_availability(date)
        return JsonResponse({
            'available': is_available,
            'message': '车辆可预订' if is_available else '车辆已被预订'
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({
            'available': False,
            'message': '车辆不存在'
        })

@require_POST
def create_booking_api(request):
    """
    创建预订的API端点
    """
    form = BookingForm(request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                
                # 发送确认邮件
                send_booking_confirmation.delay(booking.id)
                
                return JsonResponse({
                    'status': 'success',
                    'booking_id': booking.id
                })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({
        'status': 'error',
        'message': form.errors
    })
```

### 4. 缓存处理流程

#### 缓存配置：
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

#### 缓存使用示例：
```python
from django.core.cache import cache

def get_vehicle_info(vehicle_id):
    """
    获取车辆信息，使用缓存
    """
    cache_key = f'vehicle_info_{vehicle_id}'
    
    # 尝试从缓存获取
    vehicle_info = cache.get(cache_key)
    if vehicle_info is None:
        # 缓存未命中，从数据库获取
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle_info = {
                'id': vehicle.id,
                'type': vehicle.type,
                'status': vehicle.status,
                'price': str(vehicle.price)
            }
            # 设置缓存，有效期1小时
            cache.set(cache_key, vehicle_info, 3600)
        except Vehicle.DoesNotExist:
            return None
    
    return vehicle_info
``` 