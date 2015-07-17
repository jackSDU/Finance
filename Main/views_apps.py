from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect

from Main.views import ren2res
from Main.views import paginate
from Main.models import *

# the main page of app,show the app list
@login_required
def apps(req):
    if not req.user.is_superuser:
            return HttpResponseRedirect('/info/not_admin')
    if req.method == 'GET':
        p = App.objects.filter(hide=False).order_by("id")
        return ren2res("apps/apps_list.html", req, paginate(req, p))

@login_required
def app(req, n):
    if not req.user.is_superuser:
            return HttpResponseRedirect('/info/not_admin')
    if req.method == 'GET':
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
        return HttpResponseRedirect('/info/not_admin')
    hostlist = Host.objects.all()
    # GET method requests a deploy page
    if req.method == 'GET':
        return ren2res("apps/apps_deploy.html", req, {'host': hostlist})
    # request to deploy a new application
    elif req.method == 'POST':
        # add application info to app table
        info = app_info_check(req)
        if info['err']:
            return ren2res("apps/apps_deploy.html",req,{'host': hostlist, 'err': info['err']})
        uid = req.user.id
        app_submit = info['submit']
        app_submit.uid_id = uid
        # add valid args to para table
        args = app_arg_check(req)
        if args['err']:
            return ren2res("apps/apps_deploy.html", req, {'host': hostlist, 'err': args['err']})
        app_submit.save()
        app_id = app_submit.id
        for x in args['list_submit']:
            x.app_id = app_id
            x.save()
        return ren2res("apps/apps_deploy.html", req, {'host': hostlist, 'info': "部署成功"})


# delete an app deployed
@login_required
def delete(req, n):
    if not req.user.is_superuser:
            return HttpResponseRedirect('/info/not_admin')
    if req.method == 'GET':
    # If there is not an app whose id = n ,raise 404
        try:
            app = App.objects.get(id=n)
        except:
            raise Http404()
        app.hide = 1
        app.save()
        return HttpResponseRedirect('/apps/')


# modify an app deployed
@login_required
def modify(req, n):
    if not req.user.is_superuser:
            return HttpResponseRedirect('/info/not_admin')
    # ignore GET method
    if req.method == 'POST':
        # If there is not an app whose id = n ,raise 404
        try:
            app = App.objects.get(id=n)
        except:
            raise Http404()
        # check the info
        info = app_info_check(req, n)
        param = Param.objects.filter(app_id=n).order_by("order")
        # if some errors, return error warning
        if info['err']:
            hostlist = Host.objects.all().order_by("id")
            dict = {"app_i": app, "param_i": param, 'host': hostlist, 'err':info['err']}
            return ren2res("apps/apps_detail.html", req, dict)
        app_submit = info['submit']
        # check the parameters
        args = app_arg_check(req)
        if args['err']:
            hostlist = Host.objects.all()
            dict = {"app_i": app, "param_i": param, 'host': hostlist, 'err': args['err']}
            return ren2res("apps/apps_detail.html", req, dict)
        # uid is id of who deploy the app at first
        app_submit.uid_id = app.uid_id
        app_submit.save()
        param.delete()
        for x in args['list_submit']:
            x.app_id = n
            x.save()
        return HttpResponseRedirect("/apps/")

# check name,path, if one is empty, return error in err field, else insert or update a record without save()
# save() will be executed after passing parameters check
# note:same name is allowed
def app_info_check(req, app_id=None):
    dict = {'err': ""}
    name = req.POST.get('name').strip()
    if name == "":
        dict.update(err="无效的应用名称")
        return dict
    host = req.POST.get('host')
    host_id = host[host.rfind('(') + 1:-1]
    path = req.POST.get('path').strip()
    if path == "":
        dict.update(err="无效的路径")
        return dict
    desc = req.POST.get('description').strip()
    submit = App(id=app_id, name=name, host_id=host_id, path=path, desc=desc)
    dict.update(submit=submit)
    return dict

# check parameters, if a empty name or same names found, return error warning
# else insert records without save()
# save() will be executed after save() of info executed and an ID returned(deploy)
# or old parameters deleted(modify)
def app_arg_check(req):
    i = 1
    dict = {'err': ""}
    list_submit = []
    list_name = []
    while not (req.POST.get('argname' + str(i)) is None):
        order = str(i)
        argname = req.POST.get('argname' + order).strip()
        if argname == "":
            dict.update(err="无效的参数名称")
            return dict
        if argname in list_name:
            dict.update(err="重复的参数名称")
            return dict
        list_name.append(argname)
        value = req.POST.get('value' + order).strip()
        blank = 1 if req.POST.get('blank' + order) == '是' else 0
        submit = Param(order=order, name=argname, value=value, blank=blank)
        list_submit.append(submit)
        i += 1
    dict.update(list_submit=list_submit)
    return dict