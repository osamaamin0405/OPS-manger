from datetime import timezone
from django.db import models
import datetime
import random
import os
# Create your models here.


def generate_unique_name(path):
    def wrapper(instance, filename):
        extension = "." + filename.split('.')[-1]
        filename = str(random.randint(10, 99)) + str(random.randint(10, 99)) + \
            str(random.randint(10, 99)) + \
            str(random.randint(10, 99)) + \
            str(datetime.datetime.now().timestamp()) + extension
        return os.path.join(path, filename)
    return wrapper


class AdminUsers(models.Model):
    id = models.IntegerField(
        primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=30, unique=True)
    password = models.TextField(max_length=500)
    premission = models.SmallIntegerField()
    userImgae = models.ImageField(
        upload_to=generate_unique_name("uploads/userimage/"))
    dataCreated = models.DateTimeField(default=datetime.datetime.now())
