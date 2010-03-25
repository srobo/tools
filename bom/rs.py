# -*- coding: utf-8 -*-
"""Routines for scraping data about parts from RS"""
from urllib import urlopen
import string, sgmllib, sys, re, os, hashlib, time
from decimal import Decimal

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
        page = urlopen(url).read()
        f = open( F, "w" )
        f.write(page)
        f.close()

    return page

class Item(sgmllib.SGMLParser):
    "Represents a RS item"

    def __init__(self, partNumber, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.qty_range = []
        self.cost = []
        self.inside_td_element = 0
        self.inside_th_element = 0
        self.qty = True
        self.qty_str = ""

        self.prices = []

        self.feed(self.__getData(partNumber))
        self.close()

    def __getData(self, partNumber):
        page = grab_url_cached( 'http://xgoat.com/p/rs/'+str(partNumber) )

        start = string.find(page, 'id="stockY"')
        if start != -1:
            self.avail = 'In stock'
        else:
            start = string.find(page, 'Temporarily out of stock -')
            info = page[start:]
            end = string.find(info, '\n')
            self.avail = self._parse_availability(info[:end])

        start = string.find(page, '<table id="productdatatable"')
        if start == -1:
            raise Exception( """Part number "%s" doesn't exist""" % str(partNumber) )

        info = page[start:]
        end = string.find(info, '</table>')
        priceInfo = info[:end]

        return priceInfo

    def start_td(self, attributes):
        "Process a table div."
        self.inside_td_element += 1

    def end_td(self):
        "Record the end of a table div."
        self.inside_td_element -= 1

    def start_th(self, attributes):
        "Process a table heading."
        self.inside_th_element += 1

    def end_th(self):
        "Record the end of a table heading."
        self.inside_th_element -= 1

    def handle_data(self, data):
        "Handle the textual 'data'."

        data = data.replace('\n', '').replace('\r', '').replace(':', '').replace('\t', '')
        if data.replace(' ', '') == '':
            return

        if self.inside_td_element > 0:
            # print 'td:"'+data+'"'
            if "£" in data:
                # print "\tQTY_STR: \"%s\"" % self.qty_str
                # print "\tPRICE: \"%s\"" % data
                self._add_price_range( self.qty_str, data[2:] )
                self.qty_str = ""
            else:
                self.qty_str += data

        elif self.inside_th_element > 0 and data[9:13] == 'Each':
            # print 'th:"'+data+'"'
            self.multi = self._parse_pack_size(data[9:-1])

    def _parse_availability(self, s):
        "Figure out how many they've got, if they say"
        r = re.compile( "despatch ([0-9]{2})\/([0-9]{2})\/([0-9]{4})" )
        m = r.search( s )
        if m == None:
            return 'Unknown, presume out of stock'
        return 'Out of stock, due '+str(m.group(3))+'-'+str(m.group(2))+'-'+str(m.group(1))

    def _parse_pack_size(self, s):
        "Break the 'price for' string up"
        if s == 'Each':
            return 1
        r = re.compile( "Each \(In a Pack of ([0-9,]+)\)" )
        m = r.search( s )
        if m != None:
            # Strip commas
            n = m.group(1).replace(",","")
            return int(n)

        print """Warning: RS script can't parse price_for field "%s".""" % s

    def _add_price_range(self, qty, cost):
        # print "_add_price_range( qty = \"%s\", cost = \"%s\" )" % (qty, cost)
        q = self._parse_qty(qty)
        c = self._parse_cost(cost)

        if q == None:
            return

        # print "\tq: %i" % q
        # print "\tc: %s" % c

        self.prices.append( (q,c) )

    def _parse_qty(self, qty):
        r = re.compile( "([0-9,]+)\s*-\s*([0-9,]+)" )
        m = r.search(qty)
        if m != None:
            # Strip commas
            t = int(m.group(2).replace(",",""))

            # Only use the higher end of the range
            return t

        r = re.compile( "([0-9]{1}[0-9,.]*)" )
        m = r.search(qty)
        if m != None:
            # Strip commas
            t = int(m.group(1).replace(",",""))
            return t

        print """Warning: RS script can't parse quantity field: "%s".""" % qty

    def _parse_cost(self, cost):
        r = re.compile( "([0-9]{1}[0-9,.]*)" )
        m = r.search(cost)
        if m != None:
            # Strip commas
            t = m.group(1).replace(",","")
            return Decimal(t)

    def get_info(self):
        "Return a dict of the info garnered."
        return dict(qty=self.qty_range, price=self.cost, multiple=self.multi, availability=self.avail)

    def print_info(self):
        "Print a the info garnered in a nice way."
        print ' Availability:',self.avail
        print ' Order Multiple:',self.multi
        print ' Pricing:'

        n = self.prices[0][0]
        price = self.prices[0][1]
        for p in self.prices:
            if p[0] != self.multi:
                print "\t%i - %i: \t£%s" % (n, p[0] - self.multi, price)
            n = p[0]
            price = p[1]
        print "\t%i +: \t£%s" % (n, price)

