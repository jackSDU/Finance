# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('desc', models.TextField(blank=True, max_length=200)),
                ('path', models.FilePathField(recursive=True, verbose_name='/home/shixun')),
                ('hide', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ip', models.IPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Finished'), (1, 'Waiting'), (2, 'Running'), (3, 'Wrong')], default=1)),
                ('app', models.ForeignKey(to='Main.App')),
            ],
        ),
        migrations.CreateModel(
            name='JobParam',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('job', models.ForeignKey(to='Main.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=50, null=True)),
                ('value', models.CharField(blank=True, max_length=200)),
                ('blank', models.BooleanField(default=False)),
                ('app', models.ForeignKey(to='Main.App')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Priv',
            fields=[
                ('uid', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('user_manage', models.BooleanField(default=False)),
                ('jobs_manage', models.BooleanField(default=False)),
                ('data_query', models.BooleanField(default=True)),
                ('data_down', models.BooleanField(default=False)),
                ('apps_deploy', models.BooleanField(default=False)),
                ('apps_manage', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='jobparam',
            name='param',
            field=models.ForeignKey(to='Main.Param'),
        ),
        migrations.AddField(
            model_name='job',
            name='uid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='app',
            name='host',
            field=models.ForeignKey(to='Main.Host'),
        ),
        migrations.AddField(
            model_name='app',
            name='uid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
