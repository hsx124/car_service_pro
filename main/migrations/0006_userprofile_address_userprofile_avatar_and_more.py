<<<<<<< HEAD
# Generated by Django 5.1.5 on 2025-01-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_driver_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_enabled',
            field=models.BooleanField(default=True, verbose_name='启用通知'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(choices=[('zh-hans', '中文'), ('en', 'English'), ('ja', '日本語')], default='zh-hans', max_length=10, verbose_name='偏好语言'),
        ),
    ]
=======
# Generated by Django 5.1.5 on 2025-01-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_driver_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_enabled',
            field=models.BooleanField(default=True, verbose_name='启用通知'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(choices=[('zh-hans', '中文'), ('en', 'English'), ('ja', '日本語')], default='zh-hans', max_length=10, verbose_name='偏好语言'),
        ),
    ]
>>>>>>> 29e35e4892c15854585299d3eee6ff215d96cbb2
