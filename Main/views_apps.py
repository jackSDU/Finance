from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.models import *

# Create your views here.

def apps(req):##the main page of app,show the app list>>>>>


    return ren2res("apps/apps_list.html",req)

def app(req,n):
   return

def deploy(req):
    #get list of all hosts
    hostlist = Host.objects.all()
    #request to deploy page
    if req.method == 'GET':
        return ren2res("apps/apps_deploy.html",req,{'host':hostlist})
    #request to deploy a new application
    elif req.method == 'POST':
    #add application info to app table
        name = req.POST.get('name')
        host = req.POST.get('host')
        host_id = host[host.rfind('(')+1:-1]
        path = req.POST.get('path')
        desc = req.POST.get('description')
        uid = req.POST.get('uid')
        app_submit = App(name = name, desc = desc, path = path, host_id = host_id, uid_id = uid)
        app_submit.save()
        app_id=app_submit.id
    #add parameter info to para table
        i = 1
        while not (req.POST.get('argname'+str(i)) is None):
            print(111111)
            order = i
            print(order)
            argname = req.POST.get('argname'+str(i))
            value = req.POST.get('value'+str(i))
            print(req.POST.get('blank'+str(i)))
            print(req.POST.get('blank'+str(i) == 'True'))
            blank =  1 if req.POST.get('blank'+str(i)) == '是' else 0
            submit = Param(order = order, name = argname, value = value, blank = blank, app_id = app_id)
            submit.save()
            i += 1
        return ren2res("apps/apps_deploy.html",req,{'host':hostlist})


def modify(req,n):
    return

##url(r'^apps/$',views.home),                 #apps list
##url(r'^apps/([0-9]+)/$',views.home),        #detail of specified app
##url(r'^apps/deploy/$',views.home),          #deploy app
## url(r'^apps/modify/([0-9]+)/$',views.home), #modify specified app
