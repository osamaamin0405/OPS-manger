# Generated by Django 3.1.2 on 2020-11-03 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_manger', '0004_auto_20201103_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesesmanger',
            name='createdDate',
        ),
    ]