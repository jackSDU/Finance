from django.utils import timezone

from Main.models import Job

import requests

COUNT_MAX = 3

count=0

list=[]

def start(id=None):
    global count
    if id:
        list.append(id)
    while count<COUNT_MAX and len(list)>0:
        id=list.pop(0)
        job=Job.objects.get(pk=int(id))
        if job.status != 1:
            continue
        requests.post("http://"+str(job.app.host.ip)+':'+str(job.app.host.port)+'/start/'+str(job.pk)+'/',
                      {'cmd':str(job.app.path)+' '+str(job.cmd)})
        count+=1
        job.status=2
        job.start_time=timezone.now()
        job.save()

def stop(id):
    job=Job.objects.get(pk=int(id))
    if job.status != 3 and job.status != 4:
        return
    r=requests.post("http://"+str(job.app.host.ip)+':'+str(job.app.host.port)+'/stop/'+str(job.pk)+'/')
    job.status=4
    job.save()
