from math import ceil

from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.contrib import auth

from Main.models import *

def ren2res(template,req,dict={}):
    if req.user.is_authenticated():
        dict.update({'user':{'id':req.user.id,'name':req.user.get_username()}})
    else:
        dict.update(user=False)
    if req:
        return render_to_response(template,dict,context_instance=RequestContext(req))
    else:
        return render_to_response(template,dict)

def paginate(req,qs,num=None,r=5):
    cur=req.GET.get('pg')
    cur=int(cur)if cur else 1
    if not num:
        num=req.COOKIES.get('pgnum')
    num=int(num)if num else 10
    if num<1:
        num=10
    cnt=ceil(qs.count()/num+1)
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
            User.objects.create_user(req.POST['name'],req.POST['email'],req.POST['pw'])
        except:
            return ren2res("register.html",req,{'err':"The username has been used."})
        auth.login(req,auth.authenticate(username=req.POST['name'],password=req.POST['pw']))
        return HttpResponseRedirect("/")

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
            auth.login(req,user)
            next=req.session.get('next')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/')
        else:
            return ren2res("login.html",req,{'err': "Wrong username or password!"})

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')

def home(req):
    return ren2res("home.html",req)
