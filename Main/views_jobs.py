from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from Main.views import ren2res
from Main.models import *
from Main.views import paginate
from Main import client

# Create your views here.
@login_required
def choose(req):
    if req.method=='GET':
        if App.objects.exists():
            return ren2res("jobs/choose.html",req,{'apps':App.objects.all()})
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
    if req.method=='GET':
        try:

            job=Job.objects.get(id=jid)
        except:
            raise Http404()
        dict={'job':job}
        try:
            out=open("out_"+str(job.id))
            dict.update(out=out.read())
            out.close()
        except:
            dict.update(out="")
        try:
            err=open("err_"+str(job.id))
            dict.update(err=err.read())
            err.close()
        except:
            dict.update(err="")
        return ren2res("jobs/detail.html",req,dict)

def stop(req,jid):
    if req.method=='GET':
        client.stop(jid)
        return HttpResponseRedirect("/jobs/")



