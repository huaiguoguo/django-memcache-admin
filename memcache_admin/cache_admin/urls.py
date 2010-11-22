#! /usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from cache_admin.views import *

urlpatterns = patterns('',
    url(r'^$', server_list, name='cache_index'),
    url(r'^key/$', index, name='key_index'),
    url(r'^key/delete/$', delete_key, name='cache_delete'),

)
