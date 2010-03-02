#!/usr/bin/env python

# shorty.py - simple URL shortener WSGI app with Beaker cache backend
# (c) Copyright 2010 Aleksandar Radulovic. All Rights Reserved.

import bobo
import webob
from random import  sample
from string import digits, ascii_letters
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
tcache = cache.get_cache("stuff", type='dbm', expire=3600)

def short_id(num): return "".join(sample(digits + ascii_letters, num))

@bobo.post('/')
def post(url):
    id = short_id(5)
    tcache.put(id, url)
    return id

@bobo.query('/:short', method="GET")
def query(short):
    if tcache.has_key(short):
        return bobo.redirect(str(tcache.get_value(short)))
    else:
        return webob.Response("not found, sorry", status=404)

application = bobo.Application(bobo_resources=__name__)
