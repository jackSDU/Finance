from django.contrib.auth.decorators import login_required

from Main.views import ren2res
from Main.models_data import *

from datetime import date

# Create your views here.

def interest_rate(req):
    if req.method=='GET':
        qs=InterestRate.objects.using('data').all()[:10]
    #    if req.GET.get('sdate'):
    #        err=req.GET.get('sdate')
        return ren2res('data/interest_rate.html',req,{'item':qs,'err':req.GET.get('sdate')})