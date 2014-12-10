"""Routines for grabbing a page, with caching."""
import hashlib
import os
import time

from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlopen

from sr.tools.environment import get_cache_dir

# Number of seconds for the cache to last for
CACHE_LIFE = 36000


def grab_url_cached(url):
    """
    Download a possibly cached URL.

    :returns: The contents of the page.
    """
    cache_dir = get_cache_dir('urls')

    h = hashlib.sha1()
    h.update(url.encode('UTF-8'))

    F = os.path.join(cache_dir, h.hexdigest())

    if os.path.exists(F) and (time.time() - os.path.getmtime(F)) < CACHE_LIFE:
        with open(F) as file:
            page = file.read()
    else:
        # try the remote supplier page cache
        try:
            base_url = "https://www.studentrobotics.org/~rspanton/supcache/{}"
            cached_url = base_url.format(h.hexdigest())
            sc = urlopen(cached_url)
            page = sc.read()
        except HTTPError:
            page = urlopen(url).read()

        with open(F, 'wb') as file:
            file.write(page)

    return page
