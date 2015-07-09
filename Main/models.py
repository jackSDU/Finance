from django.db import models
from django.contrib.auth.models import User

from Finance.settings import APP_DEPLOY_DIR

# Create your models here.

"""Priv in heaven
class Priv(models.Model):
    uid=models.OneToOneField(User,primary_key=True)

    user_manage=models.BooleanField(default=False)

    jobs_manage=models.BooleanField(default=False)

    data_query=models.BooleanField(default=True)
    data_down=models.BooleanField(default=False)

    apps_deploy=models.BooleanField(default=False)
    apps_manage=models.BooleanField(default=False)

    def __str__(self):
        return str(self.uid)
"""

class Host(models.Model):
    name=models.CharField(max_length=30)
    ip=models.IPAddressField()

    def __str__(self):
        return str(self.name)

class App(models.Model):
    uid=models.ForeignKey(User)

    name=models.CharField(max_length=30)
    desc=models.TextField(max_length=200,blank=True)

    host=models.ForeignKey(Host)
    path=models.FilePathField(APP_DEPLOY_DIR,recursive=True)

    hide=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class Param(models.Model):
    app=models.ForeignKey(App)

    order=models.PositiveSmallIntegerField()

    name=models.CharField(max_length=50,null=True)
    value=models.CharField(max_length=200,blank=True)
    blank=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name).join(' -- ').join(str(self.app))

    class Meta:
        ordering=['order']

class Job(models.Model):
    uid=models.ForeignKey(User)
    app=models.ForeignKey(App)

    add_time=models.DateTimeField(auto_now_add=True)
    start_time=models.DateTimeField(null=True)
    end_time=models.DateTimeField(null=True)

    JOB_STATUS_CHOICES=(
        (0,'Finished'),
        (1,'Waiting'),
        (2,'Running'),
        (3,'Wrong'),
    )

    status=models.PositiveSmallIntegerField(default=1,choices=JOB_STATUS_CHOICES)

    def __str__(self):
        return str(self.uid).join(' -- ').join(str(self.app))

class JobParam(models.Model):
    job=models.ForeignKey(Job)
    param=models.ForeignKey(Param)

    value=models.CharField(max_length=200)
