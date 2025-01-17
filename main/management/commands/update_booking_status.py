from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Booking
from datetime import timedelta

class Command(BaseCommand):
    help = '自动更新预订状态'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始更新预订状态...')
        now = timezone.now()

        # 更新已确认的预订为进行中
        confirmed_bookings = Booking.objects.filter(
            status='confirmed',
            pickup_time__lte=now,
            pickup_time__gte=now - timedelta(hours=4)  # 4小时内的预订
        )
        for booking in confirmed_bookings:
            booking.status = 'in_progress'
            booking.save()
            self.stdout.write(f'预订 #{booking.id} 已更新为进行中')

        # 更新进行中的预订为已完成
        in_progress_bookings = Booking.objects.filter(
            status='in_progress',
            pickup_time__lte=now - timedelta(hours=4)  # 超过4小时的预订
        )
        for booking in in_progress_bookings:
            booking.status = 'completed'
            booking.save()
            
            # 释放车辆和司机
            if booking.vehicle:
                booking.vehicle.status = 'available'
                booking.vehicle.save()
            if booking.driver:
                booking.driver.is_available = True
                booking.driver.save()
                
            self.stdout.write(f'预订 #{booking.id} 已更新为已完成')

        # 自动取消超时未确认的预订
        pending_timeout = now - timedelta(hours=24)  # 24小时未确认自动取消
        pending_bookings = Booking.objects.filter(
            status='pending',
            created_at__lte=pending_timeout
        )
        for booking in pending_bookings:
            booking.status = 'cancelled'
            booking.save()
            
            # 释放车辆和司机
            if booking.vehicle:
                booking.vehicle.status = 'available'
                booking.vehicle.save()
            if booking.driver:
                booking.driver.is_available = True
                booking.driver.save()
                
            self.stdout.write(f'预订 #{booking.id} 因超时未确认已自动取消')

        self.stdout.write(self.style.SUCCESS('预订状态更新完成！')) 