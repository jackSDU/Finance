from django.db import models
from django.contrib.auth.models import User

from Finance.settings import APP_DEPLOY_DIR,SERVANT_PORT

# Create your models here.

class Host(models.Model):
    name=models.CharField(max_length=30)
    ip=models.GenericIPAddressField()
    port=models.PositiveSmallIntegerField(default=SERVANT_PORT)

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

    cmd=models.TextField()

    add_time=models.DateTimeField(auto_now_add=True)
    start_time=models.DateTimeField(null=True)
    end_time=models.DateTimeField(null=True)

    JOB_STATUS_CHOICES=(
        (-2,'Wrong'),
        (-1,'Stopped'),
        (0,'Finished'),
        (1,'Waiting'),
        (2,'Running'),
    )

    status=models.SmallIntegerField(default=1,choices=JOB_STATUS_CHOICES)

    def __str__(self):
        return str(self.uid).join(' -- ').join(str(self.app))
