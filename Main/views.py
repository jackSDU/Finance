##                       _oo0oo_
##                      o8888888o
##                      88" . "88
##                      (| -_- |)
##                      0\  =  /0
##                    ___/`---'\___
##                  .' \\|     |// '.
##                 / \\|||  :  |||// \
##                / _||||| -:- |||||- \
##               |   | \\\  -  /// |   |
##               | \_|  ''\---/''  |_/ |
##               \  .-\__  '-'  ___/-. /
##             ___'. .'  /--.--\  `. .'___
##          ."" '<  `.___\_<|>_/___.' >' "".
##         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
##         \  \ `_.   \_ __\ /__ _/   .-` /  /
##     =====`-.____`.___ \_____/___.-`___.-'=====
##                       `=---='
##
##
##     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##
##               佛祖保佑         永无BUG
import os
from math import ceil

from django.utils import timezone
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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
    if type(qs)==list:
        cnt=ceil(len(qs)/num)
    else:
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
            return ren2res("home.html",req,{'action':"login"})
        else:
            return HttpResponseRedirect("/")
    elif req.method=='POST':
        user=auth.authenticate(username=req.POST.get('name'),password=req.POST.get('pw'))
        if user is not None:
            if not user.is_active:
                if user.last_login:
                    return ren2res("home.html",req,{'loginerr':"用户已被删除。",'action':"login"})
                else:
                    return HttpResponseRedirect('/info/not_active/')
            auth.login(req,user)
            next=req.session.get('next')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/')
        else:
            return ren2res("home.html",req,{'loginerr':"用户名或密码错误。",'action':"login"})

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')

def home(req):
    return ren2res("home.html",req)

def page_not_found(req):
    return render_to_response("info/404.html",{'jump':False})

def registered(req):
    return render_to_response("info/registered.html",{'jump':'/'})

def not_active(req):
    return render_to_response("info/not_active.html",{'jump':'/'})

def not_admin(req):
    return render_to_response("info/not_admin.html",{'jump':req.GET.get('next')})

@require_POST
@csrf_exempt
def started(req,id):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status <= 0 and job.status!=-1:
        return HttpResponse()
    if job.status != 2:
        return HttpResponseBadRequest()
    job.status=3
    job.start_time=timezone.now()
    job.save()
    return HttpResponse()

@require_POST
@csrf_exempt
def stopped(req,id):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status <= 0 and job.status !=-1:
        return HttpResponse()
    if job.status != 4:
        return HttpResponseBadRequest()
    job.status=-1
    job.end_time=timezone.now()
    job.save()
    return HttpResponse()

@require_POST
@csrf_exempt
def finished(req,id,ok):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status != 2 and job.status != 3 and job.status != 4:
        return HttpResponseBadRequest()
    #打开输出和错误文件，写入输出和错误
    f=open(os.path.join(RESULT_DIR,'out_'+str(id)),mode='w')
    f.write(req.POST.get('out',''))
    f.close()
    f=open(os.path.join(RESULT_DIR,'err_'+str(id)),mode='w')
    f.write(req.POST.get('err',''))
    f.close()
    ret=req.POST.get('ret')
    try:
        ret=int(ret)
        job.ret=ret
    except:
        pass
    job.status=(0 if ok else -2)
    job.end_time=timezone.now()#作业结束时间
    job.save()
    client.count-=1
    client.start()
    return HttpResponse()
