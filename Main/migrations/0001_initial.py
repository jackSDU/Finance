# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priv',
            fields=[
                ('uid', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('user', models.BooleanField(default=False)),
                ('jobs', models.BooleanField(default=True)),
                ('data', models.BooleanField(default=True)),
                ('apps', models.BooleanField(default=True)),
                ('user_mod', models.BooleanField(default=False)),
                ('jobs_mod', models.BooleanField(default=False)),
                ('data_mod', models.BooleanField(default=False)),
                ('apps_mod', models.BooleanField(default=False)),
            ],
        ),
    ]
