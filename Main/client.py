from multiprocessing import Pipe

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
        scon.send((do_start,(str(job.app.host.ip),int(job.app.host.port),
                          int(job.pk),str(job.app.path),str(job.cmd),),))
        count+=1

def stop(id):
    job=Job.objects.get(pk=int(id))
    scon.send((do_stop,(str(job.app.host.ip),int(job.app.host.port),int(job.pk),),))

def do_start(ip,port,id,exec,param):
    url="http://"+ip+':'+str(port)+'/start/'+str(id)
    r=requests.post(url,{'cmd':exec+' '+param})

def do_stop(ip,port,id):
    url="http://"+ip+':'+str(port)+'/start/'+str(id)
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