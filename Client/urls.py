from django.conf.urls import url

from Client import views

urlpatterns = [
    url(r'^succeed/([0-9]+)/$',views.succeed),
    url(r'^stopped/([0-9]+)/$',views.stopped),
    url(r'^failed/([0-9]+)/$',views.failed),
]