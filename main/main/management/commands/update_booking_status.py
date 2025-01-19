from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Booking
from datetime import timedelta
import pytz
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = '自动更新预订状态'

    def handle(self, *args, **options):
        self.stdout.write('Starting to update booking status...')
        
        # Get current time in local timezone
        local_tz = pytz.timezone('Asia/Shanghai')
        current_time = timezone.localtime()
        
        self.stdout.write(f'Current time: {current_time}')
        
        # Update confirmed bookings to in_progress
        confirmed_bookings = Booking.objects.filter(
            status='confirmed',
            pickup_time__lte=current_time
        )
        
        for booking in confirmed_bookings:
            booking.status = 'in_progress'
            booking.save()
            self.stdout.write(f'Updated booking #{booking.id} to in_progress')
        
        self.stdout.write(f'Found {confirmed_bookings.count()} bookings to update to in_progress')
        
        # Update in_progress bookings to completed
        in_progress_bookings = Booking.objects.filter(
            status='in_progress',
            pickup_time__lte=current_time - timezone.timedelta(hours=2)
        )
        
        for booking in in_progress_bookings:
            booking.status = 'completed'
            booking.save()
            self.stdout.write(f'Updated booking #{booking.id} to completed')
            
        self.stdout.write(f'Found {in_progress_bookings.count()} bookings to update to completed')
        
        # Auto cancel pending bookings that are overdue
        pending_bookings = Booking.objects.filter(
            status='pending',
            created_at__lte=current_time - timezone.timedelta(hours=24)
        )
        
        for booking in pending_bookings:
            booking.status = 'cancelled'
            booking.save()
            
            # Send email notification
            try:
                subject = '预订自动取消通知'
                message = f'''
尊敬的用户：

您的预订 #{booking.id} 因超过24小时未确认，已被系统自动取消。

预订详情：
- 预订号：#{booking.id}
- 接送时间：{timezone.localtime(booking.pickup_time).strftime('%Y-%m-%d %H:%M')}
- 起点：{booking.pickup_location}
- 终点：{booking.dropoff_location}

如果您仍需要用车服务，请重新提交预订。

此致，
车辆服务团队
'''
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.user.email],
                    fail_silently=False,
                )
                self.stdout.write(f'Sent cancellation email for booking #{booking.id}')
            except Exception as e:
                self.stdout.write(f'Failed to send cancellation email for booking #{booking.id}: {str(e)}')
            
            self.stdout.write(f'Auto cancelled booking #{booking.id}')
            
        self.stdout.write(f'Found {pending_bookings.count()} bookings to auto cancel')
        
        self.stdout.write('Booking status update completed') 