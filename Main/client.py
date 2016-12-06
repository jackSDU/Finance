#client.py连接计算服务器，执行作业，获取作业结果
#
#
from django.utils import timezone
from Main.models import Job
import requests
import pexpect
from pexpect import pxssh
from multiprocessing import Process,Pipe
CLIENT_HOST="127.0.0.1"#作业结果返回本机IP
CLIENT_PORT=80#Apache监视端口
COUNT_MAX = 25#最大作业数限制

count=0#全局变量，当前运行中的作业数
list=[]#作业id列表
processs={}#进程存储字典
#开始执行作业
def start(id=None):
    global count
    if id:
        list.append(id)
    while count<COUNT_MAX and len(list)>0:
        id=list.pop(0)
        job=Job.objects.get(pk=int(id))
        if job.status != 1:
            continue
        cmd=str(job.app.path)+' '+str(job.cmd)
        username=str(job.app.host.username)
        ip=str(job.app.host.ip)
        passwd=(job.app.host.password)
        
        print ("Begin.......")
        #连接计算服务器，执行cmd命令
        p=Process(target=auto_ssh_cmd,args=(id,ip,username,passwd,cmd))
        processs[str(id)]=p
        p.start()
        print('cmd',str(job.app.path)+' '+str(job.cmd))
        count+=1
        job.status=2
        job.start_time=timezone.now()
        job.save()
#停止id作业
def stop(id):
    global count
    job=Job.objects.get(pk=int(id))
    if job.status != 3 and job.status != 4:
        return
    p=processs.pop(str(id))
    p.terminate()#进程中断
    count-=1 
    job.status=4
    job.save()
    requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+'/api/stopped/'+str(id)+'/')
#连接计算服务器，执行cmd命令
def auto_ssh_cmd(id,ip,username,passwd,cmd): 
    out=''
    err='' 
    ret=-1
    try:  
        remote = pxssh.pxssh()  
        remote.login(ip,username,passwd)  
        requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+'/api/started/'+str(id)+'/')
        remote.sendline(cmd)  
        remote.prompt() 
        r=remote.before#cmd执行结果
        remote.sendline("echo $?")#echo $?，上一条命令执行后的退出状态
        remote.prompt() 
        sta=remote.before
        status=sta.decode('utf-8')
        print(status)
        if status[-3]=='0':
            ret=0
            out=r.decode('utf-8')
        else:
            ret=-1
            err=r.decode('utf-8')
        remote.logout()  
    except pxssh.ExceptionPxssh as e:  
        err=str(e)
        ret=-2
    finally:
        requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+"/api/"+("right/" if ret==0 else "wrong/")+str(id)+'/',
                          {"out":out,"err":err,"ret":ret})#将运算结果返回

