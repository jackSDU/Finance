from multiprocessing import Pipe
from datetime import datetime

import requests

from Main.models import Job

COUNT_MAX = 3

count=0

list=[]

rcon,scon=Pipe(False)

def start(id=None):
    global count
    if id:
        list.append(id)
    while count<COUNT_MAX and len(list)>0:
        id=list.pop(0)
        job=Job.objects.get(pk=int(id))
        if job.status != 1:
            continue
        scon.send((do_start,(str(job.app.host.ip),int(job.app.host.port),
                          int(job.pk),str(job.app.path),str(job.cmd),),))
        count+=1
        job.status=2
        job.start_time=datetime.utcnow()
        job.save()

def stop(id):
    job=Job.objects.get(pk=int(id))
    if job.status != 3 and job.status != 4:
        return
    scon.send((do_stop,(str(job.app.host.ip),int(job.app.host.port),int(job.pk),),))
    job.status=4
    job.save()

def do_start(ip,port,id,exec,param):
    url="http://"+ip+':'+str(port)+'/start/'+str(id)
    r=requests.post(url,{'cmd':exec+' '+param})

def do_stop(ip,port,id):
    url="http://"+ip+':'+str(port)+'/stop/'+str(id)
    r=requests.post(url)

def daemon(rcon):
    try:
        while True:
            o=rcon.recv()
            try:
                o[0](*o[1])
            except:
                pass
    except:
        pass
