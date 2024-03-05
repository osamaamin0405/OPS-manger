from django.db import models
from django.utils.timezone import now
# Create your models here.


class PayedProducts(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateTimeField(default=now())
    productID = models.TextField()
    opNum = models.IntegerField()
    price = models.TextField()
    discound = models.DecimalField(
        max_digits=10000, decimal_places=2, default=0.0)
    total = models.TextField()
    payeduser = models.IntegerField()
    count = models.TextField()
    lastTotal = models.DecimalField(
        max_digits=10000, decimal_places=2, default=price)
