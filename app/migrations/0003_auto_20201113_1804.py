# Generated by Django 3.1.3 on 2020-11-13 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_questions_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
        migrations.RemoveField(
            model_name='users',
            name='login',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]