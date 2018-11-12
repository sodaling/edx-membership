# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 06:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import openedx.core.djangoapps.xmodule_django.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPCourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', openedx.core.djangoapps.xmodule_django.models.CourseKeyField(db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VIPInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateField(auto_now_add=True)),
                ('expired_at', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vip_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VIPOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('month', models.IntegerField()),
                ('trans_at', models.DateTimeField(auto_now_add=True)),
                ('start_at', models.DateField()),
                ('expired_at', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'Awaiting for payment'), (2, 'Paid'), (3, 'Cancelled'), (4, 'Refunded')])),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=30)),
                ('suggested_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=30)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('refno', models.CharField(max_length=255, null=True)),
                ('openid', models.CharField(max_length=128, null=True)),
                ('outtradeno', models.CharField(max_length=120, null=True)),
                ('pay_type', models.IntegerField(choices=[(5, 'Balance'), (0, 'Offline'), (1, 'WeChat'), (2, 'Alipay '), (3, 'Union pay'), (4, 'Apple Pay')])),
                ('receipt', models.TextField(null=True)),
                ('version', models.CharField(max_length=255, null=True)),
                ('os_version', models.CharField(max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vip_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VIPPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('month', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=30)),
                ('suggested_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=30)),
            ],
        ),
    ]
