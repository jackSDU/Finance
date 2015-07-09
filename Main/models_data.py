from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RawIV(models.Model):

    class Meta:
        managed=False

class IVIndex(models.Model):

    class Meta:
        managed=False

class InterestRate(models.Model):
    trade_date=models.DateField()
    currency=models.CharField(max_length=3)
    period=models.IntegerField()
    rate=models.FloatField()
    calc_date=models.DateField()

    class Meta:
        db_table='interest_rate'
        managed=False

class YieldRate(models.Model):

    class Meta:
        managed=False