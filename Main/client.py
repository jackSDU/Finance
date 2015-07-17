from multiprocessing import Pipe,Process

import requests

from Main.models import Job

COUNT_MAX = 3

count=0

rcon,scon=Pipe(False)

def start(id):
    job=Job.objects.get(pk=int(id))
    scon.send((do_start,(str(job.app.host.ip),int(job.app.host.port),
                      int(job.pk),str(job.app.path),str(job.cmd))))

def stop(id):
    job=Job.objects.get(pk=int(id))
    scon.send((do_stop,(str(job.app.host.ip),int(job.app.host.port),int(job.pk))))

def do_start(ip,port,id,exec,param):
    pass

def do_stop(ip,port,id):
    pass

def daemon(rcon):
    while True:
        o=rcon.recv()
        try:
            o[0](*o[1])
        except:
            pass

p=Process(name="daemon",target=daemon,args=(rcon))
p.daemon=True
p.start()