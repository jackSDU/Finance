from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.db.models import F

from Main.views import ren2res,paginate
from Main.models_data import *

USE_DB='data'

def render(template,req,qs,field='trade_date'):
    q=QueryDict(mutable=True)
    dict={}
    qs=qs.using(USE_DB).annotate(the_filter_date=F(field))
    sd=req.GET.get('sdate')
    if sd:
        q['sdate']=sd
        dict.update(sdate=sd)
        sd=datetime.strptime(sd,"%Y-%m-%d")
        qs=qs.filter(the_filter_date__gte=sd)
    ed=req.GET.get('edate')
    if ed:
        q['edate']=ed
        dict.update(edate=ed)
        ed=datetime.strptime(ed,"%Y-%m-%d")
        qs=qs.filter(the_filter_date__lte=ed)
    dict.update(paginate(req,qs))
    return ren2res(template,req,dict)

# Create your views here.

@login_required
def interest_rate(req):
    if req.method=='GET':
        return render('data/interest_rate.html',req,InterestRate.objects.all())

@login_required
def iv_index(req):
    if req.method=='GET':
        return render('data/iv_index.html',req,IVIndex.objects.all())

@login_required
def iv_record(req):
    if req.method=='GET':
        return render('data/iv_record.html',req,RawIV.objects.all())

@login_required
def yield_rate(req):
    if req.method=='GET':
        return render('data/yield_rate.html',req,YieldRate.objects.all())
