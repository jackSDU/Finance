from multiprocessing import Queue,Process
from urllib import request

from Main.models import Job,Host,App

COUNT_MAX = 3

queue = Queue()

count=0

def start(id):
    job=Job.objects.get(pk=int(id))
    queue.put_nowait((do_start,(str(job.app.host.ip),int(job.app.host.port),
                      int(job.pk),str(job.app.path),str(job.cmd))))

def stop(id):
    job=Job.objects.get(pk=int(id))
    queue.put_nowait((do_stop,(str(job.app.host.ip),int(job.app.host.port),int(job.pk))))

def do_start(ip,port,id,exec,param):
    pass

def do_stop(ip,port,id):
    pass

def worker():
    while True:
        op=queue.get()
        op[0](*op[1])

proc = Process(name="process",target=worker,daemon=True)

proc.start()