#! /usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from cache_admin.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),

)
