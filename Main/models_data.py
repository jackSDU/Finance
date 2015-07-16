from django.db import models

# Create your models here.

class RawIV(models.Model):
    symbol=models.CharField(max_length=3)
    exchange=models.CharField(max_length=4)
    trade_date=models.DateField()
    stock_close_price=models.FloatField()
    option_symbol=models.CharField(max_length=5)
    expiration=models.DateField()
    strike=models.FloatField()
    call_or_put=models.CharField(max_length=1)
    ask=models.FloatField()
    bid=models.FloatField()
    mean_price=models.FloatField()
    iv=models.FloatField()
    volume=models.IntegerField()
    stock_price_for_iv=models.FloatField()
    isinterpolated=models.CharField(max_length=1)
    delta=models.FloatField()
    vega=models.FloatField()
    gamma=models.FloatField()
    theta=models.FloatField()
    rho=models.FloatField()

    class Meta:
        db_table='raw_iv'
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
    trade_date=models.DateField()
    symbol=models.CharField(max_length=3)
    yield_rate=models.FloatField()
    calc_date=models.DateField()

    class Meta:
        db_table='yield_rate'
        managed=False