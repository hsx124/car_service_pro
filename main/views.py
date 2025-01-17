from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import activate, gettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Driver, ServiceArea, Vehicle, UserProfile, FAQ, Booking, Review
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    return render(request, 'main/home.html')

def booking(request):
    """预订页面视图"""
    if request.method == 'POST':
        # 检查用户是否登录
        if not request.user.is_authenticated:
            messages.error(request, _('请先登录后再进行预订。'))
            return redirect('login')
            
        # 获取表单数据
        car_type = request.POST.get('car_type')
        pickup_location = request.POST.get('pickup_location')
        destination = request.POST.get('destination')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        passengers = request.POST.get('passengers')
        luggage = request.POST.get('luggage')
        special_requests = request.POST.get('special_requests', '')
        
        # 验证必填字段
        if not all([car_type, pickup_location, destination, pickup_date, pickup_time, passengers, luggage]):
            messages.error(request, _('请填写所有必填字段。'))
            return render(request, 'main/booking.html')
            
        try:
            # 组合日期和时间
            pickup_datetime = timezone.datetime.strptime(
                f"{pickup_date} {pickup_time}", 
                "%Y-%m-%d %H:%M"
            ).replace(tzinfo=timezone.get_current_timezone())
            
            # 检查预订时间是否合理（至少提前2小时预订）
            if pickup_datetime <= timezone.now() + timedelta(hours=2):
                messages.error(request, _('请至少提前2小时预订用车。'))
                return render(request, 'main/booking.html')
                
            # 查找可用车辆
            vehicle = Vehicle.objects.filter(
                type=car_type,
                status='available'
            ).first()
            
            if not vehicle:
                messages.error(request, _('抱歉，当前没有可用的车辆，请稍后重试。'))
                return render(request, 'main/booking.html')
                
            # 查找可用司机
            driver = Driver.objects.filter(
                is_available=True,
                preferred_vehicle_types__in=[car_type, 'all']
            ).order_by('?').first()
            
            if not driver:
                messages.error(request, _('抱歉，当前没有可用的司机，请稍后重试。'))
                return render(request, 'main/booking.html')
                
            # 计算预估价格（这里使用简单的计算方式，实际应该更复杂）
            base_price = {
                'economy': 200,
                'business': 300,
                'luxury': 500
            }.get(car_type, 200)
            
            # 创建预订记录
            booking = Booking.objects.create(
                user=request.user,
                vehicle=vehicle,
                driver=driver,
                pickup_location=pickup_location,
                destination=destination,
                pickup_time=pickup_datetime,
                passengers=passengers.split('-')[0],  # 取区间的最小值
                luggage=luggage.split('-')[0] if luggage != '0' else 0,
                status='pending',
                price=base_price,
                special_requests=special_requests
            )
            
            # 更新车辆和司机状态
            vehicle.status = 'in_use'
            vehicle.save()
            driver.is_available = False
            driver.save()
            
            # 发送预订确认邮件
            send_booking_confirmation_email(booking)
            
            messages.success(request, _('预订成功！我们会尽快确认您的订单。'))
            return redirect('my_bookings')
            
        except Exception as e:
            print(f"预订错误: {str(e)}")
            messages.error(request, _('预订失败，请稍后重试。'))
            return render(request, 'main/booking.html')
    
    # GET请求显示预订表单
    return render(request, 'main/booking.html')

def send_booking_confirmation_email(booking):
    """发送预订确认邮件"""
    subject = _('您的用车预订已提交')
    message = f"""
    尊敬的 {booking.user.get_full_name()}：

    感谢您使用我们的用车服务。您的预订信息如下：

    预订编号：#{booking.id}
    上车地点：{booking.pickup_location}
    目的地：{booking.destination}
    上车时间：{timezone.localtime(booking.pickup_time).strftime('%Y-%m-%d %H:%M')}
    车型：{booking.vehicle.get_type_display()}
    车牌号：{booking.vehicle.plate_number}
    司机：{booking.driver.user.get_full_name()}
    预估价格：￥{booking.price}

    我们会尽快确认您的订单。如有任何问题，请随时联系我们的客服。

    此致
    Car Service Pro 团队
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"发送预订确认邮件失败: {str(e)}")

def drivers(request):
    return render(request, 'main/drivers.html')

def service_area(request):
    return render(request, 'main/service_area.html')

def safety(request):
    return render(request, 'main/safety.html')

def about(request):
    """关于我们页面"""
    return render(request, 'main/about.html')

def faq(request):
    """FAQ页面视图"""
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'created_at')
    return render(request, 'main/faq.html', {'faqs': faqs})

def contact(request):
    """联系我们页面"""
    if request.method == 'POST':
        # 获取客户端IP
        client_ip = request.META.get('REMOTE_ADDR')
        
        # 检查提交频率
        submission_key = f'contact_submission_{client_ip}'
        last_submission = cache.get(submission_key)
        
        if last_submission:
            # 限制每60秒只能提交一次
            time_passed = timezone.now() - last_submission
            if time_passed < timedelta(seconds=60):
                messages.error(request, _('提交过于频繁，请稍后再试。'))
                return render(request, 'main/contact.html')
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # 验证必填字段
        if not all([name, email, phone, subject, message]):
            messages.error(request, _('请填写所有必填字段。'))
            return render(request, 'main/contact.html')
        
        # 基本的垃圾内容检查
        spam_words = ['viagra', 'casino', 'lottery', 'prize', 'winner']
        if any(word in message.lower() for word in spam_words):
            messages.error(request, _('您的留言包含不适当的内容。'))
            return render(request, 'main/contact.html')
        
        try:
            # 发送邮件通知
            email_subject = f'{settings.EMAIL_SUBJECT_PREFIX}新的联系表单提交: {subject}'
            email_message = f"""
            收到新的联系表单提交：
            
            姓名: {name}
            邮箱: {email}
            电话: {phone}
            主题: {subject}
            
            留言内容:
            {message}
            
            ---
            提交IP: {client_ip}
            提交时间: {timezone.now()}
            ---
            此邮件由系统自动发送，请勿直接回复。
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            # 发送确认邮件给用户
            user_subject = _('感谢您的留言')
            user_message = f"""
            尊敬的 {name}：
            
            感谢您的留言。我们已收到您的信息，将尽快与您联系。
            
            您的留言内容：
            {message}
            
            如有任何疑问，请随时联系我们。
            
            此致
            Car Service Pro 团队
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            
            # 记录提交时间
            cache.set(submission_key, timezone.now(), 300)  # 缓存5分钟
            
            messages.success(request, _('您的留言已成功提交，我们会尽快与您联系。'))
            
        except Exception as e:
            messages.error(request, _('提交失败，请稍后重试或直接联系我们。'))
            print(f"邮件发送错误: {str(e)}")
            
    return render(request, 'main/contact.html')

def privacy(request):
    """隐私政策页面"""
    return render(request, 'main/privacy.html')

def terms(request):
    """服务条款页面"""
    return render(request, 'main/terms.html')

@login_required
def profile(request):
    """用户个人资料页面"""
    if request.method == 'POST':
        # 获取或创建用户档案
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # 处理头像上传
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        # 更新用户基本信息
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # 更新用户档案信息
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.bio = request.POST.get('bio', '')
        profile.preferred_language = request.POST.get('preferred_language', 'zh-hans')
        profile.notification_enabled = request.POST.get('notification_enabled') == 'on'
        profile.save()
        
        messages.success(request, _('个人资料已更新。'))
        return redirect('profile')
        
    return render(request, 'main/profile.html')

@login_required
def my_bookings(request):
    """用户预订历史页面"""
    # 获取状态筛选参数
    status = request.GET.get('status', 'all')
    
    # 获取用户的预订记录
    bookings = Booking.objects.filter(user=request.user)
    
    # 根据状态筛选
    if status != 'all':
        bookings = bookings.filter(status=status)
    
    # 按创建时间倒序排序
    bookings = bookings.order_by('-created_at')
    
    # 分页
    paginator = Paginator(bookings, 10)  # 每页显示10条记录
    page = request.GET.get('page')
    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        bookings = paginator.page(1)
    except EmptyPage:
        bookings = paginator.page(paginator.num_pages)
    
    context = {
        'bookings': bookings,
        'is_paginated': bookings.has_other_pages(),
        'page_obj': bookings,
    }
    
    return render(request, 'main/my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """取消预订"""
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        # 只能取消待确认或已确认的预订
        if booking.status not in ['pending', 'confirmed']:
            messages.error(request, _('只能取消待确认或已确认的预订。'))
            return redirect('my_bookings')
        
        # 更新预订状态
        booking.status = 'cancelled'
        booking.save()
        
        # 释放车辆和司机
        if booking.vehicle:
            booking.vehicle.status = 'available'
            booking.vehicle.save()
        if booking.driver:
            booking.driver.is_available = True
            booking.driver.save()
        
        # 发送取消确认邮件
        send_booking_cancellation_email(booking)
        
        messages.success(request, _('预订已成功取消。'))
        
    except Booking.DoesNotExist:
        messages.error(request, _('预订不存在。'))
    
    return redirect('my_bookings')

def send_booking_cancellation_email(booking):
    """发送预订取消确认邮件"""
    subject = _('您的预订已取消')
    message = f"""
    尊敬的 {booking.user.get_full_name()}：

    您的预订 #{booking.id} 已成功取消。

    预订详情：
    上车地点：{booking.pickup_location}
    目的地：{booking.destination}
    上车时间：{timezone.localtime(booking.pickup_time).strftime('%Y-%m-%d %H:%M')}
    车型：{booking.vehicle.get_type_display()}

    如果您改变主意，欢迎随时重新预订。
    如有任何问题，请随时联系我们的客服。

    此致
    Car Service Pro 团队
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"发送预订取消确认邮件失败: {str(e)}")

def set_language(request):
    lang = request.GET.get('lang', 'zh-hans')
    activate(lang)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))
    response.set_cookie('django_language', lang)
    return response

class DriverListView(ListView):
    model = Driver
    template_name = 'main/drivers.html'
    context_object_name = 'drivers'
    paginate_by = 9

    def get_queryset(self):
        queryset = Driver.objects.filter(is_available=True)
        
        # 驾龄筛选
        experience = self.request.GET.get('experience')
        if experience:
            if experience == '3-5':
                queryset = queryset.filter(experience_years__gte=3, experience_years__lte=5)
            elif experience == '5-10':
                queryset = queryset.filter(experience_years__gte=5, experience_years__lte=10)
            elif experience == '10+':
                queryset = queryset.filter(experience_years__gt=10)

        # 评分筛选
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating__gte=float(rating))

        return queryset.order_by('-rating', '-experience_years')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience'] = self.request.GET.get('experience', '')
        context['rating'] = self.request.GET.get('rating', '')
        return context

# 更新原来的drivers视图函数
drivers = DriverListView.as_view()

class ServiceAreaListView(ListView):
    model = ServiceArea
    template_name = 'main/service_area.html'
    context_object_name = 'service_areas'

    def get_queryset(self):
        return ServiceArea.objects.filter(is_active=True).order_by('name')

# 更新原来的service_area视图函数
service_area = ServiceAreaListView.as_view()

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'main/vehicles.html'
    context_object_name = 'vehicles'
    paginate_by = 9

    def get_queryset(self):
        queryset = Vehicle.objects.filter(status='available')
        
        # 车型筛选
        vehicle_type = self.request.GET.get('type')
        if vehicle_type:
            queryset = queryset.filter(type=vehicle_type)

        # 座位数筛选
        seats = self.request.GET.get('seats')
        if seats:
            queryset = queryset.filter(seats=seats)

        return queryset.order_by('type', 'brand')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type', '')
        context['seats'] = self.request.GET.get('seats', '')
        return context

# 更新vehicles视图函数
vehicles = VehicleListView.as_view()

@login_required
def add_review(request, booking_id):
    """添加预订评价"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # 检查预订是否已完成且未评价
    if booking.status != 'completed':
        messages.error(request, _('只能对已完成的预订进行评价。'))
        return redirect('my_bookings')
        
    if hasattr(booking, 'review'):
        messages.error(request, _('该预订已经评价过了。'))
        return redirect('my_bookings')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, _('请填写评分和评价内容。'))
            return render(request, 'main/add_review.html', {'booking': booking})
            
        try:
            Review.objects.create(
                booking=booking,
                rating=rating,
                comment=comment
            )
            messages.success(request, _('评价提交成功，感谢您的反馈！'))
            return redirect('my_bookings')
            
        except Exception as e:
            print(f"评价提交错误: {str(e)}")
            messages.error(request, _('评价提交失败，请稍后重试。'))
            
    return render(request, 'main/add_review.html', {'booking': booking})
