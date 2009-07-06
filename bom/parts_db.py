#!/usr/bin/env python
"""Student Robotics parts database access library"""
import csv

class Db(dict):
    def __init__(self, fname):
        f = open(fname, "r")
        r = csv.DictReader(f)

        for line in r:
            if line["sr-code"].strip()[0] == "#":
                continue
            c = line["sr-code"].lower()
            # Remove the code from the dictionary
            del line["sr-code"]

            for k in line.keys():
                if isinstance(line[k], str):
                    line[k] = line[k].strip()

            self[c] = line


        


