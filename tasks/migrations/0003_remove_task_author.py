# Generated by Django 4.2.6 on 2023-11-12 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='author',
        ),
    ]
