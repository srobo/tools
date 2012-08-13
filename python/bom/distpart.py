# -*- coding: utf-8 -*-
# Superclass for distributor items

class NonExistentPart(Exception):
    pass

class DistItem(object):
    def __init__(self, part_number):
        self.part_number = part_number

        # The number of items currently available
        # None <- Unknown
        # False <- Discontinued -- i.e. never going to be available
        # True <- Some in stock, but we don't know how many
        # [int] <- The number that are in stock
        self.avail = None

        # The minimum number of this item that one can order
        # (None <- Unknown)
        self.min_order = None

        # The number of components per item
        # e.g. for an item that's a 5000 component reel, this 
        # number is 5000.
        # (None <- Unknown)
        self.price_for = None

        # The smallest quantity increment that one can make
        # (None <- Unknown)
        self.multi = None

        # List of prices
        # 2-entry tuples -- (quantity, unit price)
        self.prices = None

    def print_info(self):
        print "Part", self.part_number

        print "\tStock:",
        if self.avail == None:
            print "Unknown"
        elif self.avail == False:
            print "Discontinued"
        elif self.avail == True:
            print "In stock"
        else:
            print "%i in stock" % self.avail

        print "\tMinimum order: %i" % self.min_order

        print "\tComponents per item: %i" % self.price_for

        print "\tOrder multiple: %i" % self.multi

        print "\tPricing:"

        for i in range(0, len(self.prices)):

            quantity, price = self.prices[i]
            
            if i+1 < len(self.prices):
                n_quant = self.prices[i+1][0]

                print "\t\t %i - %i: £%s" % (quantity, n_quant - self.multi, price)
            else:
                print "\t\t %i+: £%s" % (quantity, price)
