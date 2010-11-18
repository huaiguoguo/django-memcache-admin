#! /usr/bin/env python
#coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context

def index(request):
    return render_to_response('index.html', RequestContext(request, locals())) 