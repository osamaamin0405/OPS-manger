# Generated by Django 3.1.2 on 2020-11-15 21:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('receiptmanger', '0012_auto_20201115_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reciptsmanger',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 15, 21, 53, 44, 368006, tzinfo=utc)),
        ),
    ]
