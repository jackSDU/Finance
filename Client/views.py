from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.views.decorators.http import require_POST

from datetime import datetime

from Finance.settings import RESULT_DIR
from Main.models import Job

@require_POST
def succeed(req,id):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status != 2 and job.status != 3:
        return HttpResponseBadRequest()
    f=open(RESULT_DIR+'out_'+str(id),mode='w')
    f.write(req.POST.get('out'))
    f.close()
    f=open(RESULT_DIR+'err_'+str(id),mode='w')
    f.write(req.POST.get('err'))
    f.close()
    job.status=0
    job.end_time=datetime.utcnow()
    job.save()
    return HttpResponse()

@require_POST
def stopped(req,id):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status != 3:
        return HttpResponseBadRequest()
    job.status=-1
    job.end_time=datetime.utcnow()
    job.save()
    return HttpResponse()

@require_POST
def failed(req,id):
    try:
        job=Job.objects.get(pk=id)
    except:
        return HttpResponseNotFound()
    if job.status != 2 and job.status != 3:
        return HttpResponseBadRequest()
    f=open(RESULT_DIR+'out_'+str(id),mode='w')
    f.write(req.POST.get('out'))
    f.close()
    f=open(RESULT_DIR+'err_'+str(id),mode='w')
    f.write(req.POST.get('err'))
    f.close()
    job.status=0
    job.end_time=datetime.utcnow()
    job.save()
    return HttpResponse()