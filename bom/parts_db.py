#!/usr/bin/env python
"""Student Robotics parts database access library"""
import csv

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
