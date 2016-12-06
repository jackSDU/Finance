from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from Main.views import ren2res
from Main.models import *
from Main.views import paginate
from Main import client
import os
from Finance.settings import RESULT_DIR

# Create your views here.
@login_required
def choose(req):
    if req.method=='GET':
        if App.objects.exists():
            #p = App.objects.filter(hide=False).order_by("id")
            return ren2res("jobs/choose.html",req,{'apps': App.objects.filter(hide=False).order_by("id")})
        else:
            return ren2res("jobs/choose.html",req,{'info':"抱歉，还没有可用的应用！"})

@login_required
def submit(req,aid):
    if req.method == 'GET':
        try:
            app = App.objects.get(id=aid)
        except:
            raise Http404()
        params = Param.objects.filter(app=app).filter(name__isnull=False).order_by("order")
        dict={'app':app,'params':params}
        return ren2res("jobs/submit.html",req,dict)
    elif req.method == 'POST':
        id = req.POST['id']
        params = Param.objects.filter(app=int(id)).order_by("order")
        cmd=""
        for param in params:
            value=req.POST.get(str(param.order))
            if value is None:
                cmd+=str(param.value)+" "
            elif not value.strip() and not param.blank:
                try:
                    return ren2res("jobs/submit.html",req,{'app':App.objects.get(id=aid),
                                                           'params':params.filter(name__isnull=False),
                                                           'err':"带*的参数不能为空！"})
                except:
                    raise Http404()
            else:
                cmd+=value+" "
        job=Job(uid=req.user,app_id=id,cmd=cmd.strip())
        job.save()
        client.start(job.id)
        return HttpResponseRedirect("/jobs/")

@login_required
def list(req):
    if req.method=='GET':
        jobs=Job.objects.all()
        if not req.user.is_superuser:
            jobs=jobs.filter(uid=req.user)
        if jobs.exists():
            jobs=jobs.order_by("-add_time")
            return ren2res("jobs/list.html",req,paginate(req,jobs))
        else:
            return ren2res("jobs/list.html",req,{'info':"没有提交的作业！"})

@login_required
def detail(req,jid):
    print('in xiews_job,detail!!')
    if req.method=='GET':
        print('in views_job,detail--if!!')
        try:

            job=Job.objects.get(id=jid)
        except:
            raise Http404()
        dict={'job':job}
        print(os.path.join(RESULT_DIR,'out_'+str(job.id)))
        try:
            #f=open(os.path.join(RESULT_DIR,'out_'+str(id)),mode='w')
            out=open(os.path.join(RESULT_DIR,'out_'+str(job.id)))
            #print('job.id is--',job.id)
            #print('read out_',job.id,'----',out.read)
            dict.update(out=out.read())
            out.close()
        except:##问题出在这，找不到文件
            dict.update(out="")
            print('in except of readout detail')
        try:
            err=open(os.path.join(RESULT_DIR,'err_'+str(job.id)))
           # err=open("err_"+str(job.id))
            dict.update(err=err.read())
            err.close()
        except:
            dict.update(err="")
            print('in except of readerror detail')
            
        return ren2res("jobs/detail.html",req,dict)

def stop(req,jid):
    if req.method=='GET':
        client.stop(jid)
        return HttpResponseRedirect("/jobs/")



