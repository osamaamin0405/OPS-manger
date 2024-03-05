from django.db import models

# Create your models here.


class Categorys(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    catcode = models.IntegerField(unique=True)
