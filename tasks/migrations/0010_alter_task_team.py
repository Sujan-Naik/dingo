# Generated by Django 4.2.6 on 2023-11-26 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_task_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.team'),
        ),
    ]
