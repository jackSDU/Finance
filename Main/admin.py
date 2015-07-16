from django.contrib import admin

from Main.models import *

# Register your models here.

admin.site.register(Host)
admin.site.register(App)
admin.site.register(Param)
admin.site.register(Job)