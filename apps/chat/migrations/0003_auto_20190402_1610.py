# Generated by Django 2.1.7 on 2019-04-02 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_roomcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomcode',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 16, 10, 22, 500849)),
        ),
    ]