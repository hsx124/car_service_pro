# Generated by Django 5.1.5 on 2025-01-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_driver_languages_driver_preferred_vehicle_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicearea',
            name='center_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='中心纬度'),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='center_lng',
            field=models.FloatField(blank=True, null=True, verbose_name='中心经度'),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='coordinates',
            field=models.JSONField(default=list, help_text='格式：[[lat1, lng1], [lat2, lng2], ...]', verbose_name='区域坐标'),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='zoom_level',
            field=models.IntegerField(default=12, verbose_name='缩放级别'),
        ),
    ]
