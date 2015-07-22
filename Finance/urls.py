"""Finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Main import views,views_user,views_jobs,views_data,views_apps,views_platform

urlpatterns = [
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^register/$',views.register),

    url(r'^info/registered/$',views.registered),
    url(r'^info/not_active/$',views.not_active),
    url(r'^info/not_admin/$',views.not_admin),

    url(r'^$',views.home),

    url(r'^user/$',views_user.info),                 #my user info
    url(r'^user/([0-9]+)/$',views_user.info),        #specified user info
    url(r'^user/edit/$',views_user.change),            #edit user info
    url(r'^user/list/$',views_user.list),            #list users
    url(r'^user/verify/$',views_user.verify),          #verify user
    url(r'^user/([0-9]+)/delete/$',views_user.delete), #delete user

    url(r'^jobs/$',views_jobs.list),                 #jobs list
    url(r'^jobs/([0-9]+)/$',views_jobs.detail),        #detail of job
    url(r'^jobs/([0-9]+)/stop/$',views_jobs.stop),        #stop job
    url(r'^jobs/submit/$',views_jobs.choose),          #select app
    url(r'^jobs/submit/([0-9]+)/$',views_jobs.submit), #add job using specified app

    url(r'^data/iv_record/$',views_data.iv_record),
    url(r'^data/iv_index/$',views_data.iv_index),
    url(r'^data/interest_rate/$',views_data.interest_rate),
    url(r'^data/yield_rate/$',views_data.yield_rate),
    url(r'^data/download/$',views_data.download),        #data download

    url(r'^apps/$',views_apps.apps),                 #apps list
    url(r'^apps/([0-9]+)/$',views_apps.app),        #detail of specified app
    url(r'^apps/deploy/$',views_apps.deploy),          #deploy app
    url(r'^apps/modify/([0-9]+)/$',views_apps.modify), #modify specified app
    url(r'^apps/delete/([0-9]+)/$',views_apps.delete),

    url(r'^api/started/([0-9]+)/$',views.started),
    url(r'^api/stopped/([0-9]+)/$',views.stopped),
    url(r'^api/right/([0-9]+)/$',views.finished,{'ok':True}),
    url(r'^api/wrong/([0-9]+)/$',views.finished,{'ok':False}),

    url(r'^apps/host/$',views_apps.host),
    url(r'^apps/host/add/$',views_apps.host_add),
    url(r'^apps/host/delete/([0-9]+)/$', views_apps.host_delete),

    url(r'^platform/$', views_platform.list),
    url(r'^platform/upload/$', views_platform.upload),

    url(r'^admin/', include(admin.site.urls)),
] + staticfiles_urlpatterns()

handler404 = 'Main.views.page_not_found'
