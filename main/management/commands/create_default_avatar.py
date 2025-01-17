from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os
from django.conf import settings

class Command(BaseCommand):
    help = '创建默认头像图片'

    def handle(self, *args, **kwargs):
        # 确保目录存在
        avatar_dir = os.path.join(settings.MEDIA_ROOT, 'drivers')
        os.makedirs(avatar_dir, exist_ok=True)
        
        # 创建默认头像文件路径
        avatar_path = os.path.join(avatar_dir, 'default-avatar.png')
        
        # 如果文件已存在，则跳过
        if os.path.exists(avatar_path):
            self.stdout.write(self.style.SUCCESS('默认头像已存在'))
            return
            
        # 创建一个200x200的图片
        size = (200, 200)
        image = Image.new('RGB', size, color='#f0f0f0')
        
        # 创建一个ImageDraw对象
        draw = ImageDraw.Draw(image)
        
        # 绘制一个圆形
        margin = 20
        draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill='#cccccc')
        
        # 保存图片
        image.save(avatar_path, 'PNG')
        
        self.stdout.write(self.style.SUCCESS(f'默认头像已创建: {avatar_path}')) 