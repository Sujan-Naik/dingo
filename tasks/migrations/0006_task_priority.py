# Generated by Django 4.2.6 on 2023-11-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_merge_0002_team_0004_task_author_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Backlog'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Urgent')], default=3),
        ),
    ]