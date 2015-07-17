from math import ceil
from datetime import datetime

from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.contrib import auth

from Finance.settings import RESULT_DIR

from Main.models import *
from Main import client

def ren2res(template,req,dict={}):
    if req.user.is_authenticated():
        dict.update({'user':{'id':req.user.id,'name':req.user.get_username(),'super':req.user.is_superuser}})
    else:
        dict.update(user=False)
    return render_to_response(template,dict,context_instance=RequestContext(req))

def ren2err(template,jump):
    return render_to_response(template,{'jump':jump})

def paginate(req,qs,num=None,r=5):
    cur=req.GET.get('pg')
    cur=int(cur)if cur else 1
    if not num:
        num=req.COOKIES.get('pgnum')
    num=int(num)if num else 10
    if num<1:
        num=10
    cnt=ceil(qs.count()/num)
    min=cur-r
    max=cur+r
    if min<1:
        max+=(1-min)
        min=1
    if max>cnt:
        max=cnt
    q=req.GET.copy()
    q.setlist('pg',[])
    href=q.urlencode()
    if len(href)>0:
        href=href+"&"
    href=req.path+"?"+href
    return {'href':href,'pg':cur,'pgc':cnt,'pgs':range(min,max+1),'item':qs[num*cur-num:num*cur]}

# Create your views here.

def register(req):
    if req.method=='GET':
        return ren2res("register.html",req)
    elif req.method=='POST':
        try:
            u=User.objects.create_user(req.POST['name'],req.POST['email'],req.POST['pw'])
        except:
            return ren2res("register.html",req,{'err':"用户名已被使用。"})
        u.firstname=req.POST.get('real')
        u.is_active=False
        u.save()
        return HttpResponseRedirect("/info/registered/")

def login(req):
    if req.method=='GET':
        if req.user.is_anonymous():
            if req.GET.get('next'):
                req.session['next']=req.GET.get('next')
            return ren2res("login.html",req)
        else:
            return HttpResponseRedirect("/")
    elif req.method=='POST':
        user=auth.authenticate(username=req.POST.get('name'),password=req.POST.get('pw'))
        if user is not None:
            if not user.is_active:
                if user.last_login:
                    return ren2res("login.html",req,{'err':"用户已被删除。"})
                else:
                    return HttpResponseRedirect('/err/not_active/')
            auth.login(req,user)
            next=req.session.get('next')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/')
        else:
            return ren2res("login.html",req,{'err':"用户名或密码错误。"})

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')

def home(req):
    return ren2res("home.html",req)

def page_not_found(req):
    return ren2err("info/404.html",False)

def registered(req):
    return ren2err("info/registered.html",'/')

def not_active(req):
    return ren2err("info/not_active.html",'/')

def not_admin(req):
    return ren2err("info/not_admin.html",req.GET.get('next'))

@require_POST
def finished(req,id,status):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status != 2:
        return HttpResponseBadRequest()
    f=open(RESULT_DIR+'out_'+str(id),mode='w')
    f.write(req.POST.get('out'))
    f.close()
    f=open(RESULT_DIR+'err_'+str(id),mode='w')
    f.write(req.POST.get('err'))
    f.close()
    ret=req.POST.get('ret')
    try:
        ret=int(ret)
        job.ret=ret
    except:
        pass
    if status:
        job.status=0
    else:
        job.status=-2
    job.end_time=datetime.utcnow()
    job.save()
    client.count-=1
    client.start()
    return HttpResponse()
