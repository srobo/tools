# -*- coding: utf-8 -*-
"""Routines for scraping data about parts from digikey"""
from cachedfetch import grab_url_cached

class Item:
    """Represents a Digikey item"""

    def __init__(self, partNumber):
        self.avail = 0
        self.min_order = 0
        self.price_for = 1
        self.multi = 1
        self.prices = []

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
