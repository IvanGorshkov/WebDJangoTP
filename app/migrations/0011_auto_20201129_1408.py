# Generated by Django 3.1.3 on 2020-11-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20201117_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(default='/27804.png', max_length=1024, upload_to='static/', verbose_name='Аватар'),
        ),
    ]
