# Generated by Django 3.1.2 on 2020-11-03 21:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sales_manger', '0003_auto_20201103_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesesmanger',
            name='createdDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 21, 36, 8, 728441, tzinfo=utc)),
        ),
    ]