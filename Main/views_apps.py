from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect

from Main.views import ren2res
from Main.views import paginate
from Main.models import *

##the main page of app,show the app list
@login_required
def apps(req):
    if req.method == 'GET':
        if not req.user.is_superuser:
            return HttpResponseRedirect('/err/not_admin')
        p = App.objects.filter(hide=False).order_by("id")
        return ren2res("apps/apps_list.html", req, paginate(req, p))

@login_required
def app(req, n):
    if req.method == 'GET':
        if not req.user.is_superuser:
            return HttpResponseRedirect('/err/not_admin')
        try:
            a = App.objects.get(id=n)
        except:
            raise Http404()
        p = Param.objects.filter(app_id=n).order_by("order")
        hostlist = Host.objects.all()
        return ren2res("apps/apps_detail.html", req, {"app_i": a, "param_i": p, 'host': hostlist})

@login_required
def deploy(req):
    if not req.user.is_superuser:
        return HttpResponseRedirect('/err/not_admin')
    # get list of all hosts
    hostlist = Host.objects.all()
    # request to deploy page
    if req.method == 'GET':
        return ren2res("apps/apps_deploy.html", req, {'host': hostlist})
    # request to deploy a new application
    elif req.method == 'POST':
        # add application info to app table
        name = req.POST.get('name')
        host = req.POST.get('host')
        host_id = host[host.rfind('(') + 1:-1]
        path = req.POST.get('path')
        desc = req.POST.get('description')
        uid = req.POST.get('uid')
        app_submit = App(name=name, desc=desc, path=path, host_id=host_id, uid_id=uid)
        app_submit.save()
        app_id = app_submit.id
        # add parameters info to para table
        i = 1
        while not (req.POST.get('argname' + str(i)) is None):
            order = str(i)
            argname = req.POST.get('argname' + order)
            value = req.POST.get('value' + order)
            blank = 1 if req.POST.get('blank' + order) == '是' else 0
            submit = Param(order=order, name=argname, value=value, blank=blank, app_id=app_id)
            submit.save()
            i += 1
        return ren2res("apps/apps_deploy.html", req, {'host': hostlist})


# delete an app deployed
@login_required
def delete(req, n):
    if req.method == 'GET':
        if not req.user.is_superuser:
            return HttpResponseRedirect('/err/not_admin')
        a = App.objects.get(id=n)
        a.hide = 1
        a.save()
        return HttpResponseRedirect('/apps/')


# modify an app deployed
@login_required
def modify(req, n):
    if req.method == 'POST':
        if not req.user.is_superuser:
            return HttpResponseRedirect('/err/not_admin')
        a = App.objects.get(id=n)
        len_arg = req.POST["arg_len"]
        a.name = req.POST["name"]
        a.path = req.POST["path"]
        a.desc = req.POST["description"]
        a.save()
        Param.objects.filter(app_id=n).delete()
        for i in range(1, int(len_arg) + 1):
            si = str(i)
            if req.POST["blank" + si] == "True":
                bv = 1
            else:
                bv = 0
            p = Param(order=i, name=req.POST["argname" + si], value=req.POST["value" + si], blank=bv, app_id=n)
            p.save()
        return HttpResponseRedirect("/apps/")
