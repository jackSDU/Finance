# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_auto_20160707_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FilePathField(verbose_name='D:\\#ibm Power\\2016\\项目源码\\网站源码\\Finance\\upload', recursive=True),
        ),
    ]
