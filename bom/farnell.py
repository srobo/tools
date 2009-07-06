"""Routines for scraping data about parts from Farnell"""
from urllib import urlopen
import string, sgmllib, sys

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

        self.feed(self.__getData(partNumber))
        self.close()

    def __getData(self, partNumber):
        page = urlopen('http://xgoat.com/p/farnell/'+str(partNumber)).read()

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
                self.qty_range.append(data)
                self.qty = False
            else:
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
                self.price_for = data
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
