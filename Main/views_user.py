from django.contrib.auth.decorators import login_required

from Main.views import ren2res,paginate
from Main.models import *
from django.shortcuts import render_to_response,Http404,HttpResponseRedirect
from django.contrib import auth

# Create your views here.
def info(req):
    if req.method=='GET':
        b=req.user
        super=b.is_superuser
        #email=User.objects.get(id=req.user).email
        email=b.email
        return ren2res("user/info.html",req,{'super':super,'email':email})

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

    b=req.user
    super=b.is_superuser
    a=User.objects.all()
    o=paginate(req,a,8)
    dict={'super':super}
    dict.update(o)
   # b=Priv.objects.all()
    if req.method=='GET':
        return ren2res("user/list.html",req,dict)
 #   if req.method=='POST':
#        c=User.objects.get(uid_id=req.POST['id'])
 #       c.user_manage=bool(req.POST.get('user_manage'))
 #       c.jobs_manage=bool(req.POST.get('jobs_manage'))
 #       c.data_query=bool(req.POST.get('data_query'))
  #      c.data_down=bool(req.POST.get('data_down'))
   #     c.apps_deploy=bool(req.POST.get('apps_deploy'))
    #    c.apps_manage=bool(req.POST.get('apps_manage'))
     #  return ren2res("user/list.html",req,{'a':a})

def verify(req):

    b=req.user
    super=b.is_superuser
    dict={'super':super}
    if req.method=='GET':
        a=User.objects.filter(is_active=False)
        o=paginate(req,a,8)
        dict.update(o)
        return ren2res("user/verify.html",req,dict)
    if req.method=='POST':
        a=User.objects.filter(id=req.POST['id'])
        a.is_active=True
        a.save()
        b=User.objects.filter(is_active=False)
        o=paginate(req,b)
        dict.update(o)
        return ren2res("user/verify.html",req,dict)

def infocheck(req,id):
    b=req.user
    super=b.is_superuser
    if req.method=='GET':
        u=User.objects.get(id=id)
        return ren2res("user/info_check.html",req,{'u':u,'super':super})

def delete(req,id):
    if req.method=='GET':
        a=User.objects.get(id=id)
        if a.is_superuser==False :
            a.delete()
        return HttpResponseRedirect("/user/list")