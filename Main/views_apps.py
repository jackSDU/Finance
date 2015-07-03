from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.models import *

# Create your views here.

def apps(req):##the main page of app,show the app list>>>>>
    x=priv.objects.filter(uid_id=req.user.id)
    if priv.objects.filter(uid_id=req.user.id) !=None

    return ren2res("apps/apps_list.html",req)

def app(req,n):
    return

def deploy(req):
    return ren2res("apps/apps_deploy.html",req)

def modify(req,n):
    return

##url(r'^apps/$',views.home),                 #apps list
##url(r'^apps/([0-9]+)/$',views.home),        #detail of specified app
##url(r'^apps/deploy/$',views.home),          #deploy app
## url(r'^apps/modify/([0-9]+)/$',views.home), #modify specified app

