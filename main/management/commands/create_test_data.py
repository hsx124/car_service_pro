<<<<<<< HEAD
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Vehicle, Driver, ServiceArea, FAQ, Booking
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = '创建测试数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始创建测试数据...')

        # 获取指定用户
        try:
            test_user = User.objects.get(username='hsx124')
            self.stdout.write('找到用户: hsx124')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('用户hsx124不存在！'))
            return

        # 创建车辆数据
        vehicles_data = [
            {
                'type': 'economy',
                'brand': '丰田',
                'model': '卡罗拉',
                'plate_number': '京A12345',
                'seats': 4,
                'year': 2022,
                'features': '舒适座椅、自动空调、USB充电',
            },
            {
                'type': 'business',
                'brand': '奔驰',
                'model': 'E级',
                'plate_number': '京B12345',
                'seats': 4,
                'year': 2023,
                'features': '真皮座椅、智能驾驶、无线充电',
            },
            {
                'type': 'luxury',
                'brand': '劳斯莱斯',
                'model': '幻影',
                'plate_number': '京C12345',
                'seats': 4,
                'year': 2023,
                'features': '星空顶、按摩座椅、迷你吧',
            }
        ]

        for vehicle_data in vehicles_data:
            Vehicle.objects.get_or_create(
                plate_number=vehicle_data['plate_number'],
                defaults=vehicle_data
            )
        self.stdout.write('车辆数据创建成功')

        # 创建司机数据
        drivers_data = [
            {
                'username': 'driver1',
                'password': 'driverpass123',
                'first_name': '张',
                'last_name': '师傅',
                'email': 'driver1@example.com',
                'license_number': 'BJ12345678',
                'experience_years': 5,
                'phone': '13800138001',
                'address': '北京市朝阳区',
                'bio': '有5年驾龄，熟悉北京市区路线',
                'languages': 'zh',
            },
            {
                'username': 'driver2',
                'password': 'driverpass123',
                'first_name': '佐藤',
                'last_name': '健一',
                'email': 'driver2@example.com',
                'license_number': 'BJ87654321',
                'experience_years': 8,
                'phone': '13800138002',
                'address': '北京市海淀区',
                'bio': '有8年驾龄，精通中日英三语',
                'languages': 'all',
            }
        ]

        for driver_data in drivers_data:
            user, _ = User.objects.get_or_create(
                username=driver_data['username'],
                defaults={
                    'email': driver_data['email'],
                    'first_name': driver_data['first_name'],
                    'last_name': driver_data['last_name'],
                }
            )
            user.set_password(driver_data['password'])
            user.save()

            Driver.objects.get_or_create(
                user=user,
                defaults={
                    'license_number': driver_data['license_number'],
                    'experience_years': driver_data['experience_years'],
                    'phone': driver_data['phone'],
                    'address': driver_data['address'],
                    'bio': driver_data['bio'],
                    'languages': driver_data['languages'],
                }
            )
        self.stdout.write('司机数据创建成功')

        # 创建预订数据
        vehicles = Vehicle.objects.all()
        drivers = Driver.objects.all()
        
        # 创建不同状态的预订
        booking_data = [
            {
                'status': 'pending',
                'pickup_time': timezone.now() + timedelta(days=1),
                'pickup_location': '北京首都国际机场T3航站楼',
                'destination': '北京市朝阳区国贸CBD',
                'passengers': 2,
                'luggage': 2,
                'price': 300,
            },
            {
                'status': 'confirmed',
                'pickup_time': timezone.now() + timedelta(days=2),
                'pickup_location': '北京市海淀区中关村',
                'destination': '北京大兴国际机场',
                'passengers': 3,
                'luggage': 3,
                'price': 400,
            },
            {
                'status': 'completed',
                'pickup_time': timezone.now() - timedelta(days=1),
                'pickup_location': '北京西站',
                'destination': '北京市东城区王府井',
                'passengers': 2,
                'luggage': 2,
                'price': 200,
            },
            {
                'status': 'cancelled',
                'pickup_time': timezone.now() - timedelta(days=2),
                'pickup_location': '北京南站',
                'destination': '天安门广场',
                'passengers': 4,
                'luggage': 4,
                'price': 350,
            }
        ]

        # 删除用户现有的预订记录
        Booking.objects.filter(user=test_user).delete()
        self.stdout.write('清除现有预订记录')

        # 创建新的预订记录
        for booking_info in booking_data:
            Booking.objects.create(
                user=test_user,
                vehicle=random.choice(vehicles),
                driver=random.choice(drivers),
                pickup_location=booking_info['pickup_location'],
                destination=booking_info['destination'],
                pickup_time=booking_info['pickup_time'],
                passengers=booking_info['passengers'],
                luggage=booking_info['luggage'],
                status=booking_info['status'],
                price=booking_info['price'],
            )
        self.stdout.write('预订数据创建成功')

=======
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Vehicle, Driver, ServiceArea, FAQ, Booking
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = '创建测试数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始创建测试数据...')

        # 获取指定用户
        try:
            test_user = User.objects.get(username='hsx124')
            self.stdout.write('找到用户: hsx124')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('用户hsx124不存在！'))
            return

        # 创建车辆数据
        vehicles_data = [
            {
                'type': 'economy',
                'brand': '丰田',
                'model': '卡罗拉',
                'plate_number': '京A12345',
                'seats': 4,
                'year': 2022,
                'features': '舒适座椅、自动空调、USB充电',
            },
            {
                'type': 'business',
                'brand': '奔驰',
                'model': 'E级',
                'plate_number': '京B12345',
                'seats': 4,
                'year': 2023,
                'features': '真皮座椅、智能驾驶、无线充电',
            },
            {
                'type': 'luxury',
                'brand': '劳斯莱斯',
                'model': '幻影',
                'plate_number': '京C12345',
                'seats': 4,
                'year': 2023,
                'features': '星空顶、按摩座椅、迷你吧',
            }
        ]

        for vehicle_data in vehicles_data:
            Vehicle.objects.get_or_create(
                plate_number=vehicle_data['plate_number'],
                defaults=vehicle_data
            )
        self.stdout.write('车辆数据创建成功')

        # 创建司机数据
        drivers_data = [
            {
                'username': 'driver1',
                'password': 'driverpass123',
                'first_name': '张',
                'last_name': '师傅',
                'email': 'driver1@example.com',
                'license_number': 'BJ12345678',
                'experience_years': 5,
                'phone': '13800138001',
                'address': '北京市朝阳区',
                'bio': '有5年驾龄，熟悉北京市区路线',
                'languages': 'zh',
            },
            {
                'username': 'driver2',
                'password': 'driverpass123',
                'first_name': '佐藤',
                'last_name': '健一',
                'email': 'driver2@example.com',
                'license_number': 'BJ87654321',
                'experience_years': 8,
                'phone': '13800138002',
                'address': '北京市海淀区',
                'bio': '有8年驾龄，精通中日英三语',
                'languages': 'all',
            }
        ]

        for driver_data in drivers_data:
            user, _ = User.objects.get_or_create(
                username=driver_data['username'],
                defaults={
                    'email': driver_data['email'],
                    'first_name': driver_data['first_name'],
                    'last_name': driver_data['last_name'],
                }
            )
            user.set_password(driver_data['password'])
            user.save()

            Driver.objects.get_or_create(
                user=user,
                defaults={
                    'license_number': driver_data['license_number'],
                    'experience_years': driver_data['experience_years'],
                    'phone': driver_data['phone'],
                    'address': driver_data['address'],
                    'bio': driver_data['bio'],
                    'languages': driver_data['languages'],
                }
            )
        self.stdout.write('司机数据创建成功')

        # 创建预订数据
        vehicles = Vehicle.objects.all()
        drivers = Driver.objects.all()
        
        # 创建不同状态的预订
        booking_data = [
            {
                'status': 'pending',
                'pickup_time': timezone.now() + timedelta(days=1),
                'pickup_location': '北京首都国际机场T3航站楼',
                'destination': '北京市朝阳区国贸CBD',
                'passengers': 2,
                'luggage': 2,
                'price': 300,
            },
            {
                'status': 'confirmed',
                'pickup_time': timezone.now() + timedelta(days=2),
                'pickup_location': '北京市海淀区中关村',
                'destination': '北京大兴国际机场',
                'passengers': 3,
                'luggage': 3,
                'price': 400,
            },
            {
                'status': 'completed',
                'pickup_time': timezone.now() - timedelta(days=1),
                'pickup_location': '北京西站',
                'destination': '北京市东城区王府井',
                'passengers': 2,
                'luggage': 2,
                'price': 200,
            },
            {
                'status': 'cancelled',
                'pickup_time': timezone.now() - timedelta(days=2),
                'pickup_location': '北京南站',
                'destination': '天安门广场',
                'passengers': 4,
                'luggage': 4,
                'price': 350,
            }
        ]

        # 删除用户现有的预订记录
        Booking.objects.filter(user=test_user).delete()
        self.stdout.write('清除现有预订记录')

        # 创建新的预订记录
        for booking_info in booking_data:
            Booking.objects.create(
                user=test_user,
                vehicle=random.choice(vehicles),
                driver=random.choice(drivers),
                pickup_location=booking_info['pickup_location'],
                destination=booking_info['destination'],
                pickup_time=booking_info['pickup_time'],
                passengers=booking_info['passengers'],
                luggage=booking_info['luggage'],
                status=booking_info['status'],
                price=booking_info['price'],
            )
        self.stdout.write('预订数据创建成功')

>>>>>>> 29e35e4892c15854585299d3eee6ff215d96cbb2
        self.stdout.write(self.style.SUCCESS('所有测试数据创建完成！')) 