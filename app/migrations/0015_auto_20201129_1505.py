# Generated by Django 3.1.3 on 2020-11-29 15:05

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20201129_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(default='static/27804.png', max_length=1024, upload_to=app.models.avatar_upload_to, verbose_name='Аватар'),
        ),
    ]
