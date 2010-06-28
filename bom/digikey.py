# -*- coding: utf-8 -*-
"""Routines for scraping data about parts from digikey"""
from cachedfetch import grab_url_cached
from BeautifulSoup import BeautifulSoup

class Item:
    """Represents a Digikey item"""

    def __init__(self, partNumber):
        self.avail = 0
        self.min_order = 0
        self.price_for = 1
        self.multi = 1
        self.prices = []
        self.cost = []
        self.qty_range = 0

        soup = BeautifulSoup(grab_url_cached('http://xgoat.com/p/digikey/'+str(partNumber)))

        # Extract availability
        qa_heading = soup.find(text='Quantity Available')
        if qa_heading == None:
            raise Exception("""Part number "%s" doesn't exist""" % str(partNumber))
        self.avail = int(qa_heading.findNext('td').contents[0].replace(',',''))

        # Extract order multiple
        sp_heading = soup.find(text='Standard Package')
        self.multi = int(sp_heading.parent.findNext('td').contents[0].replace(',',''))



    def get_info(self):
        """Return a dict of the info"""
        return dict(qty=self.qty_range, price=self.cost, num_for_price=self.price_for, min_order=self.min_order, multiple=self.multi, number_available=self.avail)

    def print_info(self):
        """Print all of the info on the part"""
        print ' Number Available:',self.avail
        print ' Price For:',self.price_for
        print ' Minimum Order Quantity:',self.min_order
        print ' Order Multiple:',self.multi
        print ' Pricing:'

        n = self.min_order
        for p in self.prices:
            if n != p[0]:
                print "\t%i - %i: \t£%s" % (n, p[0], p[1])
                n = p[0] + 1
            else:
                print "\t%i +: \t£%s" % (n, p[1])
