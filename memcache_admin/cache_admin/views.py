#! /usr/bin/env python
#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template.context import RequestContext, Context
from django.core.urlresolvers import reverse
from django.core.cache import cache
from utils import mcstats

def index(request):
    mcs = mcstats("localhost", 11211)
    slabCounts = mcs.calcSlabsCount(mcs.connect('stats items \r\n'))
    key_items = mcs.showKVpairs(slabCounts)
    return render_to_response('index.html', RequestContext(request, locals())) 


def delete_key(request):
    key = request.POST.get("key")
    cache.delete(key)    
    return HttpResponse("Y")