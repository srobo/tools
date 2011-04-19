# -*- coding: utf-8 -*-
"""Routines for scraping data about parts from digikey"""
from cachedfetch import grab_url_cached
from srBeautifulSoup import BeautifulSoup
from decimal import Decimal

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

        soup = BeautifulSoup(grab_url_cached('https://xgoat.com/p/digikey/'+str(partNumber)))

        # Extract availability
        qa_heading = soup.find(text='Quantity Available')
        if qa_heading == None:
            raise Exception("""Part number "%s" doesn't exist""" % str(partNumber))
        qa = qa_heading.findNext('td').contents[0].string
        if qa != None:
            self.avail = int(qa.replace(',',''))
        else:
            self.avail = 0

        # Extract order multiple
        sp_heading = soup.find(text='Standard Package')
        self.multi = int(sp_heading.parent.findNext('td').contents[0].replace(',',''))

        # Extract pricing
        # Get a list of the table rows, the first one is the heading row
        price_table_trs = soup.find(text='Price Break').parent.parent.parent.findAll('tr')
        for row in price_table_trs:
            next_row = row.nextSibling.nextSibling
            # Skip first row as it contains headings, it does however give access
            # to the minimum quantity value on the next row
            if row.find('th') != None:
                self.min_order = int(next_row.contents[0].string.replace(',',''))
                continue;
            if next_row != None:
                # Get top range of quantity from the next row
                qty = int(next_row.contents[0].string.replace(',',''))-1
            else:
                # For the last row just use its own quantity, there is no next row
                qty = int(row.contents[0].string.replace(',',''))
            cost = Decimal(row.contents[1].string)
            self.prices.append( (qty, cost) )

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
