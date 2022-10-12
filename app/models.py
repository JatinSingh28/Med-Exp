from django.db import models
from datetime import date

# Create your models here.


class Med(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiry = models.DateField(blank=True)
    # date = models.DateField(blank=True, default=date.today())
    time_left = models.IntegerField(blank=True,default=0)
    red = models.BooleanField(default=False)
    yellow = models.BooleanField(default=False)
    green = models.BooleanField(default=False)
