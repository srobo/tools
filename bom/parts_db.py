#!/usr/bin/env python
"""Student Robotics parts database access library"""
import csv, farnell

class Part(dict):
    """Represents a part"""
    def __init__(self, d):
        """Initialise from a dict from the DB"""
        c = d["sr-code"].lower()

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

    def __load_data(self):
        if self["supplier"] == "farnell":
            f = farnell.Item( self["order-number"] )
            self.stock = f.avail
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
