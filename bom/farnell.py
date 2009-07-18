"""Routines for scraping data about parts from Farnell"""
from urllib import urlopen
import string, sgmllib, sys, re, os, hashlib, time
from decimal import Decimal

# Number of seconds for the cache to last for
CACHE_LIFE = 3600

def grab_url_cached(url):
    cache_dir = os.path.expanduser( "~/.sr/cache/farnell" )

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
    "Represents a Farnell item"

    def __init__(self, partNumber, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.qty_range = []
        self.cost = []
        self.inside_td_element = 0
        self.inside_p_element = 0
        self.inside_b_element = 0
        self.last_data = ''
        self.qty = True

        self.last_qty = None
        self.prices = []

        self.feed(self.__getData(partNumber))
        self.close()

    def __getData(self, partNumber):
        page = grab_url_cached( 'http://xgoat.com/p/farnell/'+str(partNumber) )

        start = string.find(page, '<div id="availability">')
        if start == -1:
            raise Exception( """Part number "%s" doesn't exist""" % str(partNumber) )

        info = page[start:]
        end = string.find(info, '</div>')
        availInfo = info[:end]

        start = string.find(page, '<div id="price">')
        if start == -1:
            raise Exception( """Part number "%s" doesn't exist""" % str(partNumber) )

        info = page[start:]
        end = string.find(info, '</div>')
        priceInfo = info[:end]

        return availInfo+priceInfo

    def start_td(self, attributes):
        "Process a table div."
        self.inside_td_element += 1

    def end_td(self):
        "Record the end of a table div."
        self.inside_td_element -= 1

    def start_p(self, attributes):
        "Process a paragraph."
        self.inside_p_element += 1

    def end_p(self):
        "Record the end of a paragraph."
        self.inside_p_element -= 1

    def start_b(self, attributes):
        "Process a bold."
        self.inside_b_element += 1

    def end_b(self):
        "Record the end of a bold."
        self.inside_b_element -= 1

    def handle_data(self, data):
        "Handle the textual 'data'."

        data = data.replace('\n', '').replace(':', '')
        if data.replace(' ', '') == '':
            return

        if self.inside_td_element > 0:
            #	print 'td:"'+data+'"'
            if self.qty:
                self.last_qty = data

                self.qty_range.append(data)
                self.qty = False
            else:
                self._add_price_range( self.last_qty, data[2:] )
                self.last_qty = None

                self.cost.append(data[2:])
                self.qty = True

        elif self.inside_b_element > 0:
            #	print 'b:"'+data+'"'
            self.last_data = data

        elif self.inside_p_element > 0:
            #	print 'p:"'+data+'"'
            #kill off the last_data, but store it just in case
            tmp_last_data = self.last_data
            self.last_data = ''
            #test for a match to last_data
            if tmp_last_data == 'Price For':
                self.price_for = self._parse_price_for(data)
            elif tmp_last_data == 'Minimum Order Quantity':
                self.min_order = int(data)
            elif tmp_last_data == 'Order Multiple':
                self.multi = int(data)
            elif tmp_last_data == 'Availability':
                if data.isdigit():
                    self.avail = int(data)
                else:
                    self.avail = str(data)
            else:	#not this time around
                self.last_data = tmp_last_data

    def _parse_price_for(self, s):
        "Break the 'price for' string up"
        r = re.compile( "Reel of ([0-9,]+)" )
        m = r.search( s )
        if m != None:
            # Strip commas
            n = m.group(1).replace(",","")
            return int(n)

        r = re.compile( "([0-9,]+) Each" )
        m = r.search( s )
        if m != None:
            # Strip commas
            n = m.group(1).replace(",","")
            return int(n)

        print """Warning: Farnell script can't parse price_for field "%s".""" % s

    def _add_price_range(self, qty, cost):
        q = self._parse_qty(qty)
        c = self._parse_cost(cost)

        if q == None:
            return

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

        print """Warning: Farnell script can't parse quantity field: "%s".""" % qty

    def _parse_cost(self, cost):
        r = re.compile( "([0-9]{1}[0-9,.]*)" )
        m = r.search(cost)
        if m != None:
            # Strip commas
            t = m.group(1).replace(",","")
            return Decimal(t)

    def get_info(self):
        "Return a dict of the info garnered."
        return dict(qty=self.qty_range, price=self.cost, num_for_price=self.price_for, min_order=self.min_order, multiple=self.multi, number_available=self.avail)

    def print_info(self):
        "Print a the info garnered in a nice way."
        print ' Number Available:',self.avail
        print ' Price For:',self.price_for
        print ' Minimum Order Quantity:',self.min_order
        print ' Order Multiple:',self.multi
        print ' Pricing:'
        for i in range(0, len(self.qty_range)):
            print ' ',self.qty_range[i],'  \t',self.cost[i]
