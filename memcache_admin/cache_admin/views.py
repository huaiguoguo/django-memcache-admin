#! /usr/bin/env python
#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template.context import RequestContext, Context
from django.core.urlresolvers import reverse
from django.core.cache import cache
from utils import mcstats
from django.conf import settings
from django.core.cache import parse_backend_uri
from utils import get_memcached_stats

_, hosts, _ = parse_backend_uri(settings.CACHE_BACKEND)
SERVERS = hosts.split(';')

def index(request):
    mcs = mcstats("localhost", 11211)
    slabCounts = mcs.calcSlabsCount(mcs.connect('stats items \r\n'))
    key_items = set(mcs.showKVpairs(slabCounts))
    key_items = [one for one in key_items if int(one[1])>20 ]
    return render_to_response('index.html', RequestContext(request, locals())) 


def delete_key(request):
    key = request.POST.get("key")
    cache.delete(key)    
    return HttpResponse("Y")

def flush_all(request):
    cache.clear()
    return HttpResponse(reverse("cache_index"))

def server_list(request):
    statuses = zip(range(len(SERVERS)), SERVERS, map(get_memcached_stats, SERVERS))
    context = {
        'statuses': statuses,
    }
    return render_to_response(
        'stats.html',
        context,
        context_instance=RequestContext(request)
    )



#def delete_many(request):
#    key = 