from django.db import models
import random
from django.utils.timezone import now

# Create your models here.


class SalesesManger(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    salesCode = models.IntegerField(unique=True)
