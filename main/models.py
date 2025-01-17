from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Vehicle(models.Model):
    """车辆信息模型"""
    TYPE_CHOICES = [
        ('economy', _('经济型')),
        ('business', _('商务型')),
        ('luxury', _('豪华型')),
    ]

    STATUS_CHOICES = [
        ('available', _('可用')),
        ('in_use', _('使用中')),
        ('maintenance', _('维护中')),
    ]

    type = models.CharField(_('车型'), max_length=20, choices=TYPE_CHOICES)
    brand = models.CharField(_('品牌'), max_length=50)
    model = models.CharField(_('型号'), max_length=50)
    plate_number = models.CharField(_('车牌号'), max_length=20, unique=True)
    seats = models.IntegerField(_('座位数'))
    year = models.IntegerField(_('年份'))
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='available')
    features = models.TextField(_('特点'), blank=True)
    image = models.ImageField(_('图片'), upload_to='vehicles/', blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('车辆')
        verbose_name_plural = _('车辆')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"

class Driver(models.Model):
    """司机信息模型"""
    LANGUAGE_CHOICES = [
        ('zh', _('中文')),
        ('ja', _('日语')),
        ('en', _('英语')),
        ('zh_ja', _('中文和日语')),
        ('zh_en', _('中文和英语')),
        ('ja_en', _('日语和英语')),
        ('all', _('中文、日语和英语')),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('economy', _('经济型')),
        ('business', _('商务型')),
        ('luxury', _('豪华型')),
        ('all', _('全部类型')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(_('驾驶证号'), max_length=50, unique=True)
    experience_years = models.IntegerField(_('驾龄'))
    phone = models.CharField(_('联系电话'), max_length=20)
    address = models.TextField(_('地址'))
    photo = models.ImageField(_('照片'), upload_to='drivers/', null=True, blank=True, default='drivers/default-avatar.png')
    bio = models.TextField(_('个人简介'), blank=True)
    rating = models.DecimalField(_('评分'), max_digits=3, decimal_places=2, default=5.00)
    is_available = models.BooleanField(_('是否可用'), default=True)
    languages = models.CharField(_('语言'), max_length=10, choices=LANGUAGE_CHOICES, default='zh')
    preferred_vehicle_types = models.CharField(_('擅长车型'), max_length=10, choices=VEHICLE_TYPE_CHOICES, default='all')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('司机')
        verbose_name_plural = _('司机')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.license_number})"

    @property
    def recent_reviews(self):
        """获取最近的评价"""
        return self.bookings.filter(review__isnull=False).order_by('-review__created_at')[:3]

    @property
    def total_trips(self):
        """获取总行程数"""
        return self.bookings.filter(status='completed').count()

    @property
    def average_rating(self):
        """获取平均评分"""
        from django.db.models import Avg
        return self.bookings.filter(review__isnull=False).aggregate(Avg('review__rating'))['review__rating__avg'] or 5.00

class Booking(models.Model):
    """预订信息模型"""
    STATUS_CHOICES = [
        ('pending', _('待确认')),
        ('confirmed', _('已确认')),
        ('in_progress', _('进行中')),
        ('completed', _('已完成')),
        ('cancelled', _('已取消')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='bookings')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name='bookings')
    pickup_location = models.CharField(_('上车地点'), max_length=255)
    destination = models.CharField(_('目的地'), max_length=255)
    pickup_time = models.DateTimeField(_('上车时间'))
    passengers = models.IntegerField(_('乘客人数'))
    luggage = models.IntegerField(_('行李数量'))
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    special_requests = models.TextField(_('特殊要求'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('预订')
        verbose_name_plural = _('预订')
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.user.get_full_name()}"

class Review(models.Model):
    """预订评价模型"""
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(
        choices=[
            (1, '★'),
            (2, '★★'),
            (3, '★★★'),
            (4, '★★★★'),
            (5, '★★★★★'),
        ],
        verbose_name=_('评分')
    )
    comment = models.TextField(verbose_name=_('评价内容'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))

    class Meta:
        verbose_name = _('评价')
        verbose_name_plural = _('评价')
        ordering = ['-created_at']

    def __str__(self):
        return f'预订 #{self.booking.id} 的评价'

class ServiceArea(models.Model):
    """服务区域模型"""
    name = models.CharField(_('区域名称'), max_length=100)
    description = models.TextField(_('区域描述'))
    base_price = models.DecimalField(_('基础价格'), max_digits=10, decimal_places=2)
    coordinates = models.JSONField(_('区域坐标'), default=list, help_text=_('格式：[[lat1, lng1], [lat2, lng2], ...]'))
    center_lat = models.FloatField(_('中心纬度'), null=True, blank=True)
    center_lng = models.FloatField(_('中心经度'), null=True, blank=True)
    zoom_level = models.IntegerField(_('缩放级别'), default=12)
    is_active = models.BooleanField(_('是否启用'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('服务区域')
        verbose_name_plural = _('服务区域')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 如果没有设置中心点，则根据坐标计算
        if self.coordinates and not (self.center_lat and self.center_lng):
            lats = [coord[0] for coord in self.coordinates]
            lngs = [coord[1] for coord in self.coordinates]
            if lats and lngs:
                self.center_lat = sum(lats) / len(lats)
                self.center_lng = sum(lngs) / len(lngs)
        super().save(*args, **kwargs)

class FAQ(models.Model):
    """常见问题模型"""
    question = models.CharField(_('问题'), max_length=255)
    answer = models.TextField(_('答案'))
    category = models.CharField(_('分类'), max_length=50)
    order = models.IntegerField(_('排序'), default=0)
    is_active = models.BooleanField(_('是否启用'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('常见问题')
        verbose_name_plural = _('常见问题')
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.question

class Contact(models.Model):
    """联系信息模型"""
    name = models.CharField(_('姓名'), max_length=100)
    email = models.EmailField(_('邮箱'))
    phone = models.CharField(_('电话'), max_length=20)
    subject = models.CharField(_('主题'), max_length=200)
    message = models.TextField(_('消息内容'))
    is_processed = models.BooleanField(_('是否处理'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    processed_at = models.DateTimeField(_('处理时间'), null=True, blank=True)

    class Meta:
        verbose_name = _('联系信息')
        verbose_name_plural = _('联系信息')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class UserProfile(models.Model):
    """用户档案模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(_('手机号码'), max_length=20, blank=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('个人简介'), max_length=500, blank=True)
    address = models.CharField(_('地址'), max_length=200, blank=True)
    preferred_language = models.CharField(
        _('偏好语言'),
        max_length=10,
        choices=[('zh-hans', '中文'), ('en', 'English'), ('ja', '日本語')],
        default='zh-hans'
    )
    notification_enabled = models.BooleanField(_('启用通知'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('用户档案')
        verbose_name_plural = _('用户档案')

    def __str__(self):
        return f"{self.user.username}的档案"

    def get_avatar_url(self):
        """获取用户头像URL"""
        if self.avatar:
            return self.avatar.url
        return '/static/img/default-avatar.png'
