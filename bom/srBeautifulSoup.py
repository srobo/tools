import sys

def _check_bs_version():
    import BeautifulSoup as bs

    if bs.__version__[:3] == "3.1":
        print "Your BeautifulSoup version is naff.  So much of this"
        print "stuff won't work for you."
        print "Read this page for details:"
        print "http://www.crummy.com/software/BeautifulSoup/3.1-problems.html"
        sys.exit(1)

_check_bs_version()
from BeautifulSoup import *
