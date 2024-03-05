from django.db import models
import os
from datetime import datetime
import random
from django.utils.timezone import now
# Create your models here.


# def generate_unique_name(path):
#     def wrapper(instance, filename):
#         extension = "." + filename.split('.')[-1]
#         filename = str(random.randint(10, 99)) + str(random.randint(10, 99)) + \
#             str(random.randint(10, 99)) + \
#             str(random.randint(10, 99)) + \
#             str(datetime.now().timestamp()) + extension
#         return os.path.join(path, filename)
#     return wrapper


class Products(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    salesname = models.CharField(max_length=100)
    catename = models.CharField(max_length=50)
    addeduser = models.IntegerField()
    bougthprice = models.DecimalField(decimal_places=2, max_digits=100000)
    payprice = models.DecimalField(decimal_places=2, max_digits=10000)
    minconut = models.IntegerField()
    realcount = models.IntegerField()
    productimge = models.ImageField(
        upload_to="uploads/proudactImages/")
    productCode = models.CharField(max_length=50)
    date = models.DateTimeField(default=now())
    recpry = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10000)
    incr = models.DecimalField(default=0.0, decimal_places=2, max_digits=10000)


class Qrcodes(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    qrfiel = models.ImageField(upload_to="uploads/qrcodes")
