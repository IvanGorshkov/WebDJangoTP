# Generated by Django 3.1.3 on 2020-11-16 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20201114_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answers',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='views',
        ),
        migrations.AddField(
            model_name='answers',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='questions',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='answerslikes',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Отметка'),
        ),
        migrations.AlterField(
            model_name='questionslikes',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Отметка'),
        ),
    ]
