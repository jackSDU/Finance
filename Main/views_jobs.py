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
            raise Http404
        params = Param.objects.filter(app=app)
        dict={'app':app,'params':params,'length':params.count()}
        if req.GET.get("msg"):
            dict.update({'err':"带*的参数不能为空！"})
        return ren2res("jobs/submit.html",req,dict)
    elif req.method == 'POST':
        id = req.POST['id']
        params = Param.objects.filter(app=App.objects.get(id=id)).order_by("order")
        for param in params:
           value=req.POST.get(str(param.order))
           if value.strip()=="" and param.blank==False:
               return HttpResponseRedirect("?msg=err")
        cmd=""
        for param in params:
            cmd += req.POST[str(param.order)]
            cmd += " "
        job=Job(uid=req.user,app=App.objects.get(id=id),cmd=cmd.strip())
        job.save()
        client.start(job.id)
        return HttpResponseRedirect("/jobs?page=1&msg=info")

@login_required
def list(req):
    if req.method=='GET':
        if req.user.is_superuser and Job.objects.all().exists():
            job=Job.objects.all().order_by("-add_time")
        elif Job.objects.filter(uid=req.user).exists():
            job=Job.objects.filter(uid=req.user).order_by("-add_time")
        else:
            return ren2res("jobs/list.html", req, {'info':"没有提交的作业！"})
        dict=paginate(req,job)
        if req.GET.get("msg"):
            dict.update({'info':"作业提交成功!"})
        return ren2res("jobs/list.html",req,dict)

@login_required
def detail(req,jid):
    if req.method=='GET':
        try:
            job=Job.objects.get(id=jid)
        except:
            raise Http404
        try:
            with open("a.txt","r") as result:
                res=result.read()
        except IOError as error:
            res="作业还未执行完成！"
        dict={'job':job,'result':res}
        return ren2res("jobs/detail.html",req,dict)

def stop(req,jid):
    if req.method=='GET':
        client.stop(jid)



