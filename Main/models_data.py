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

    class Meta:
        managed=False

class YieldRate(models.Model):

    class Meta:
        managed=False