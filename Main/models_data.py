from django.db import models

# Create your models here.

class RawIV(models.Model):

    class Meta:
        managed=False

class IVIndex(models.Model):
    symbol=models.CharField(max_length=3)
    exchange=models.CharField(max_length=4)
    trade_date=models.DateField()
    price=models.FloatField()
    ivCall30=models.FloatField()
    ivPut30=models.FloatField()
    ivMean30=models.FloatField()
    ivCall60=models.FloatField()
    ivPut60=models.FloatField()
    ivMean60=models.FloatField()
    ivCall90=models.FloatField()
    ivPut90=models.FloatField()
    ivMean90=models.FloatField()
    ivCall120=models.FloatField()
    ivPut120=models.FloatField()
    ivMean120=models.FloatField()
    ivCall150=models.FloatField()
    ivPut150=models.FloatField()
    ivMean150=models.FloatField()
    ivCall180=models.FloatField()
    ivPut180=models.FloatField()
    ivMean180=models.FloatField()

    class Meta:
        db_table='iv_index'
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