# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.models import *
from math import ceil

# Create your views here.
def ren2res(template, req, dict={}):
    if req.user.is_authenticated():
        dict.update({'user': {'id': req.user.id, 'name': req.user.get_username()}})
    else:
        dict.update({'user': False})
    if req:
        return render_to_response(template, dict, context_instance=RequestContext(req))
    else:
        return render_to_response(template, dict)

def choose(req):
    if App.objects.exists():
        return ren2res("jobs/choose.html",req,{'apps':App.objects.all()})
    else:
        return ren2res("jobs/choose.html",req,{'info':u"抱歉，还没有可用的应用！"})

def submit(req,aid='1'):
    if req.method == 'GET':
        app = App.objects.get(id=aid)
        params = Param.objects.filter(app=app)
        dict={'app':app,'params':params,'length':params.count()}
        if req.GET.get("msg"):
            dict.update({'err':u"带*的参数不能为空！"})
        return ren2res("jobs/submit.html",req,dict)
    elif req.method == 'POST':
        id = req.POST['id']
        params = Param.objects.filter(app=App.objects.get(id=id))
        for param in params:
           value=req.POST[param.name]
           if value.strip()=="" and param.blank==False:
               return HttpResponseRedirect("?msg=err")
        #     检验有效性
        job=Job(uid=req.user,app=App.objects.get(id=id))
        job.save()
        for param in params:
            JobParam(job=job,param=param,value=req.POST[param.name]).save()
        #     启动后台线程处理job
        return HttpResponseRedirect("/jobs?page=1&msg=info")

def list(req):
    if req.user.is_superuser and Job.objects.all().exists():
        job=Job.objects.all().order_by("-add_time")
    elif Job.objects.filter(uid=req.user).exists():
        job=Job.objects.filter(uid=req.user).order_by("-add_time")
    else:
        return ren2res("jobs/list.html", req, {'info':u"没有提交的作业!"})
    limit=10
    page=int(req.GET.get("page"))
    dict={'lpages':range(1,page),'rpages':range(page+1,ceil(job.count()/limit)+1),'current':page,'pre':page-1,'next':page+1,'first':page==1,'last':page==ceil(job.count()/limit)}
    dict.update({'jobs':job[(page-1)*limit:min(page*limit,job.count())]})
    if req.GET.get("msg"):
        dict.update({'info':u"作业提交成功!"})
    return ren2res("jobs/list.html",req,dict)

def detail(req,jid='1'):
    job=Job.objects.get(id=jid)
    params=JobParam.objects.filter(job=job)
    try:
        with open("a.txt","r") as result:
            res=result.read()
    except IOError as error:
        res="The job have not finished!"
    dict={'job':job,'params':params,'result':res}
    return ren2res("jobs/detail.html",req,dict)



