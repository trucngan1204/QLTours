# Generated by Django 3.2.6 on 2021-12-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0019_auto_20211224_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default=None, upload_to='users/%Y/%m'),
        ),
    ]
