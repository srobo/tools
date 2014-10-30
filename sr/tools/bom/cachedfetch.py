# -*- coding: utf-8 -*-
"""Routines for grabbing a page, with caching"""

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

import os, hashlib, time

# Number of seconds for the cache to last for
CACHE_LIFE = 36000

def grab_url_cached(url):
    cache_dir = os.path.expanduser( "~/.sr/cache/rs" )

    if not os.path.exists( cache_dir ):
        os.makedirs( cache_dir )

    h = hashlib.sha1()
    h.update(url)

    F = os.path.join( cache_dir, h.hexdigest() )

    if os.path.exists( F ) and (time.time() - os.path.getmtime( F )) < CACHE_LIFE:
        f = open( F, "r" )
        page = f.read()
        f.close()
    else:
        # Try the remote supplier page cache
        sc = urlopen( "https://www.studentrobotics.org/~rspanton/supcache/%s" % h.hexdigest() )
        if sc.getcode() == 200:
            page = sc.read()
        else:
            page = urlopen(url).read()

        f = open( F, "w" )
        f.write(page)
        f.close()

    return page
