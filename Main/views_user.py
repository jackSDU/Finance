from django.contrib.auth.decorators import login_required

from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from Main.views import ren2res,paginate
from Main.models import *

# Create your views here.

@login_required
def info(req,id=None):
    if req.method=='GET':
        if id:
            u=User.objects.get(id=id)
        else:
            u=req.user
        super=req.user.is_superuser
        return ren2res("user/info.html",req,{'super':super,'u':u})

@login_required
def change(req):
    b=req.user
    super=b.is_superuser
    if req.method=='GET':
        return ren2res("user/change.html",req,{'super':super})
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
            return ren2res("user/change.html",req,{'err':"wrong password",'super':super})

@login_required
def list(req):
    if req.user.is_superuser:
        dict={'super':req.user.is_superuser}
        dict.update(paginate(req,User.objects.filter(is_active=True),8))
        if req.method=='GET':
            return ren2res("user/list.html",req,dict)
    else :
        return HttpResponseRedirect("/err/not_admin/")

@login_required
def verify(req):
    if not req.user.is_superuser :
        return HttpResponseRedirect("/err/not_admin/")
    dict={'super':req.user.is_superuser}
    if req.method=='GET':
        dict.update(paginate(req,User.objects.filter(is_active=False).filter(last_login__isnull=True),8))
        return ren2res("user/verify.html",req,dict)
    if req.method=='POST':
        try:
            a=User.objects.get(id=req.POST['id'])
        except ObjectDoesNotExist:
            dict.update(err="用户不存在")
            return ren2res("user/verify.html",req,dict)
        a.is_active=True
        a.save()
        dict.update(paginate(req,User.objects.filter(is_active=False),8))
        dict.update(info="修改成功")
        return ren2res("user/verify.html",req,dict)

@login_required
def delete(req,id):
    if req.method=='GET':
        a=User.objects.get(id=id)
        if a.is_superuser==False :
            if a.last_login==None:
                a.delete()
            else:
                a.is_active=False
        return HttpResponseRedirect("/user/list")