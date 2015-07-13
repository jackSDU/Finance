from django.contrib.auth.decorators import login_required

from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from Main.views import ren2res,paginate
from Main.models import *

# Create your views here.
def info(req,id=None):
    if req.method=='GET':
        if id:
            u=User.objects.get(id=id)
        else:
            u=req.user
        super=req.user.is_superuser

        return ren2res("user/info.html",req,{'super':super,'u':u})

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


def list(req):
    dict={'super':req.user.is_superuser}
    dict.update(paginate(req,User.objects.all(),8))
    if req.method=='GET':
        return ren2res("user/list.html",req,dict)

def verify(req):
    dict={'super':req.user.is_superuser}
    if req.method=='GET':
        dict.update(paginate(req,User.objects.filter(is_active=False),8))
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

def delete(req,id):
    if req.method=='GET':
        a=User.objects.get(id=id)
        if a.is_superuser==False :
            a.delete()
        return HttpResponseRedirect("/user/list")