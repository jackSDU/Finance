from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.models import *
from django.shortcuts import render_to_response,Http404,HttpResponseRedirect
from django.contrib import auth

# Create your views here.
def info(req):
    if req.method=='GET':
        a=Priv.objects.get(uid=req.user).user_manage
        #email=User.objects.get(id=req.user).email
        email=req.user.email
        return ren2res("user/info.html",req,{'a':a,'email':email})

def change(req):
    if req.method=='GET':
        return ren2res("user/change.html",req)
    if req.method=='POST':
        a=req.user
        npw=False
        if a.check_password(str(req.POST['opw'])):
            if req.POST['email']!="":
               a.email=req.POST['email']
            if req.POST['npw']!='':
                a.set_password(str(req.POST['npw']))
                npw=True
            a.save()
            if npw:
                return HttpResponseRedirect("/login/")
            else:
                return HttpResponseRedirect("/user/")
        else:
            return ren2res("user/change.html",req,{'err':"wrong password"})


def list(req):
    if req.method=='POST':
        return ren2res("user/list.html",req)