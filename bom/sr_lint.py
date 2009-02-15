#!/usr/bin/env python
import os, sys, parts_db, parts_parser

if len(sys.argv) < 3:
    print "Usage:",os.path.basename(sys.argv[0]),"PARTSLIST SR_DB"
    print "Check all components in a parts list exist."
    sys.exit(1)

inpath = sys.argv[1]
srpath = sys.argv[2]

lib = parts_db.Db(srpath)
parts = parts_parser.EagleParts(inpath)

bom = {}

error = 0
found = 0

for id in parts.keys():
    if not lib.has_key( parts[id] ):
        print "Error (%s): '%s' not in SR component database, please re-align your mind" % (id, parts[id])
        error = error + 1
    else:
        found = found + 1

print found,"parts checked in",srpath
if error > 0:
    print "Fail:", error, "parts not identified"
    sys.exit(2)


