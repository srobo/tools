#!/usr/bin/env python
"""Student Robotics parts database access library"""
import csv, farnell

class Part(dict):
    """Represents a part"""
    def __init__(self, d):
        """Initialise with a dict from the DB"""
        for k in d.keys():
            if isinstance(d[k], str):
                d[k] = d[k].strip()

        for k,v in d.iteritems():
            self[k] = v

        self.loaded = False

    def stockcheck(self):
        """Return how many of the product are in stock."""
        if not self.loaded:
            self.__load_data()

        return self.stock

    def get_price(self):
        if not self.loaded:
            self.__load_data()

        return 

    def get_dist_units(self):
        """Number of components per distributor unit"""
        if not self.loaded:
            self.__load_data()
        
        return self.dist_unit

    def get_min_order(self):
        if not self.loaded:
            self.__load_data()
        
        return self.min_order

    def get_increments(self):
        if not self.loaded:
            self.__load_data()
        
        return self.increments

    def __load_data(self):
        if self["supplier"] == "farnell":
            f = farnell.Item( self["order-number"] )
            self.stock = f.avail
            # Minimum order
            self.min_order = f.min_order
            # How many *components* per item
            # e.g. for an item that's a 5000 component reel of things, this 
            #      is 5000.  This means when asking the distributor for one of 
            #      part "XXXXX", they send a reel of 5000 components.
            self.dist_unit = f.price_for
            # Smallest quantity increment
            self.increments = f.multi
        else:
            self.stock = None
            return

        self.loaded = True

class Db(dict):
    def __init__(self, fname):
        f = open(fname, "r")
        r = csv.DictReader(f)

        for line in r:
            # Discard commented out lines
            if line["sr-code"].strip()[0] == "#":
                continue

            part = Part(line)
            self[ part["sr-code"] ] = part
