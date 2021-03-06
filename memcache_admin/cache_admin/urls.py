#! /usr/bin/env python
#coding=utf-8
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from cache_admin.views import *

urlpatterns = patterns('',
    url(r'^$', server_list, name='cache_index'),
    url(r'^server/(?P<pk>\d+)/$', index, name='server_index'),
    url(r'^key/delete/$', delete_key, name='cache_delete'),
    url(r'^flush/', flush_all, name='flush_all'),

)
