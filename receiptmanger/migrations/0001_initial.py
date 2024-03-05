# Generated by Django 3.1.2 on 2020-11-13 00:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReciptsManger',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(verbose_name=datetime.datetime(2020, 11, 13, 0, 13, 6, 724055, tzinfo=utc))),
                ('items', models.IntegerField()),
            ],
        ),
    ]
