from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import QueryDict

from Main.views import ren2res,paginate
from Main.models_data import *

def render(template,req,qs):
    q=QueryDict(mutable=True)
    dict={}
    sd=req.GET.get('sdate')
    if sd:
        q['sdate']=sd
        dict.update(sdate=sd)
        sd=datetime.strptime(sd,"%Y-%m-%d")
        qs=qs.filter(trade_date__gte=sd)
    ed=req.GET.get('edate')
    if ed:
        q['edate']=ed
        dict.update(edate=ed)
        ed=datetime.strptime(ed,"%Y-%m-%d")
        qs=qs.filter(trade_date__lte=ed)
    dict.update(paginate(req,qs))
    return ren2res(template,req,dict)

# Create your views here.

def interest_rate(req):
    if req.method=='GET':
        return render('data/interest_rate.html',req,InterestRate.objects.using('data'))