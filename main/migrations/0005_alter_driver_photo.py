# Generated by Django 5.1.5 on 2025-01-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='photo',
            field=models.ImageField(blank=True, default='drivers/default-avatar.png', null=True, upload_to='drivers/', verbose_name='照片'),
        ),
    ]