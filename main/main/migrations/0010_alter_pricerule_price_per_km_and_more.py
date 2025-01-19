# Generated by Django 4.2.18 on 2025-01-19 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_rename_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricerule',
            name='price_per_km',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='每公里价格'),
        ),
        migrations.AlterField(
            model_name='pricerule',
            name='time_period',
            field=models.CharField(choices=[('normal', '平时'), ('peak', '高峰'), ('night', '夜间'), ('holiday', '节假日')], max_length=20, verbose_name='时段'),
        ),
    ]
