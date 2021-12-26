# Generated by Django 3.2.6 on 2021-12-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0014_auto_20211222_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='tags',
        ),
        migrations.AddField(
            model_name='tour',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='Tour', to='tours.Tag'),
        ),
    ]
