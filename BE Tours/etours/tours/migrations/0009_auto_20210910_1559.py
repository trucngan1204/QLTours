# Generated by Django 3.2.6 on 2021-09-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0008_alter_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='price',
        ),
        migrations.AddField(
            model_name='tour',
            name='price_adult',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='price_child',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
