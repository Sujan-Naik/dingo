# Generated by Django 4.2.6 on 2023-12-07 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_timelogging'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelogging',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]