# Generated by Django 3.1.3 on 2020-11-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201129_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(default='/27804.png', max_length=1024, upload_to='', verbose_name='Аватар'),
        ),
    ]