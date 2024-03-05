from datetime import time
from django.db import models
from django.utils import timezone
# Create your models here.


class ReciptsManger(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    json = models.TextField()
    date = models.DateTimeField(default=timezone.now())
    items = models.IntegerField()
    catename = models.IntegerField()
    addeduser = models.IntegerField()
    total = models.DecimalField(
        default=0.0, max_digits=10000, decimal_places=3)
