from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.views import paginate
from Main.models import *

# Create your views here.
##DJango数据库操作
##p1 = Publisher(name='Apress', address='2855 Telegraph Avenue',
#       city='Berkeley', state_province='CA', country='U.S.A.',
#       website='http://www.apress.com/')
# p1.save()//插入数据

# Publisher.objects.all()//查询

#Publisher.objects.get(name="Apress")//获取单个对象

#Publisher.objects.filter(name='Apress')//筛选
#Publisher.objects.filter(name__contains="press")

#Publisher.objects.order_by("name") //排序
#Publisher.objects.order_by("-name")

#Publisher.objects.order_by('name')[0]//限制返数据
#Publisher.objects.order_by('name')[0:2]

#Publisher.objects.filter(id=52).update(name='Apress Publishing')//更新
#>>> p = Publisher.objects.get(name='Apress') #先查询
#>>> p.name = 'Apress Publishing' #更新
#>>> p.save()  #保存


#//删除
#Publisher.objects.filter(country='USA').delete()
#>>> p = Publisher.objects.get(name="O'Reilly")
#>>> p.delete()

#request.POST.get('nonexistent_field', 'Nowhere Man')
#request.POST['your_name']
##has_key(key)
#request.POST.getlist('bands')


def apps(req):##the main page of app,show the app list>>>>>
    p=App.objects.filter(hide=False).order_by("id")
    return ren2res("apps/apps_list.html",req,paginate(req,p))

def app(req,n):
    a=App.objects.get(id=n)
    p=Param.objects.filter(app_id=n).order_by("order")
    return ren2res("apps/apps_detail.html",req,{"app_i":a,"param_i":p})

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
            blank =  1 if req.POST.get('blank'+str(i)) == '鏄?' else 0
            submit = Param(order = order, name = argname, value = value, blank = blank, app_id = app_id)
            submit.save()
            i += 1
        return ren2res("apps/apps_deploy.html",req,{'host':hostlist})

def modify(req,n):
    a=App.objects.get(id=n)
    del_flag=req.POST.get("delete","False")
    if del_flag=="True":
        a.hide=1
        a.save()
        return apps(req)
    else:
        len_arg=req.POST["arg_len"]
        arr=[]
        a.name=req.POST["name"]
        a.path=req.POST["path"]
        a.desc=req.POST["description"]
        a.save()
        Param.objects.filter(app_id=n).delete()
        for i in range(1,int(len_arg)+1):
            si=str(i)
            if req.POST["blank"+si]=="True":
                bv=1
            else:
                bv=0
            arr.append({"name"+si:req.POST.get("argname"+si,"noname"),"value"+si:req.POST.get("value"+si,"novalue"),"blank"+si:req.POST.get("blank"+si,"novalue")})
            p=Param(order=i,name=req.POST["argname"+si],value=req.POST["value"+si],blank=bv,app_id=n)
            p.save()
        return apps(req)

    #return ren2res("apps/apps_list.html",req,{"length":len_arg,"arr":arr})

##url(r'^apps/$',views.home),                 #apps list
##url(r'^apps/([0-9]+)/$',views.home),        #detail of specified app
##url(r'^apps/deploy/$',views.home),          #deploy app
## url(r'^apps/modify/([0-9]+)/$',views.home), #modify specified app
