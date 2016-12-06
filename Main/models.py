from django.db import models
from django.contrib.auth.models import User

from Finance.settings import APP_DEPLOY_DIR,SERVANT_PORT,UPLOAD_DIR

# Create your models here.

#主机model
class Host(models.Model):
    name=models.CharField(max_length=30)
    ip=models.GenericIPAddressField()
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    def __str__(self):
        return str(self.name)
#应用model
class App(models.Model):
    uid=models.ForeignKey(User)

    name=models.CharField(max_length=30)
    desc=models.TextField(max_length=200,blank=True)

    host=models.ForeignKey(Host)
    path=models.FilePathField(APP_DEPLOY_DIR,recursive=True)

    hide=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
#参数model
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
#作业model
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
        (2,'Starting'),
        (3,'Running'),
        (4,'Stopping'),
    )

    status=models.SmallIntegerField(default=1,choices=JOB_STATUS_CHOICES)
    ret=models.IntegerField(null=True)

    def __str__(self):
        return str(self.uid).join(' -- ').join(str(self.app))

#文件model
class File(models.Model):
    uid = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    path = models.FilePathField(UPLOAD_DIR, recursive=True)

    def __str__(self):
        return str(self.name)
