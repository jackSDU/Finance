from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Priv(models.Model):
    uid=models.OneToOneField(User,primary_key=True)

    user=models.BooleanField(default=False)
    jobs=models.BooleanField(default=True)
    data=models.BooleanField(default=True)
    apps=models.BooleanField(default=True)

    user_mod=models.BooleanField(default=False)
    jobs_mod=models.BooleanField(default=False)
    data_mod=models.BooleanField(default=False)
    apps_mod=models.BooleanField(default=False)

    def __str(self):
        return self.uid.username