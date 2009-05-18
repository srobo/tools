#!/usr/bin/env python
import os, sys, time, parts_db, parts_parser

def html_header(f):
    f.write("""<html>
<head>
<title>Student Robotics Bill of Materials for ...</title>
<style>
td {
  border-style: solid none none none;
  border-width: 1px;
}
</style>
</head>
<body>
<p>Generated on %s with %s.</p>
<table style="border-style:none;border-spacing:0;">
<tr><th>Identifier</th><th>Description</th><th>Distributer</th><th>Distributor Order Number</th></tr>
""" % (time.asctime(), os.path.basename(sys.argv[0])) )

def html_footer(f):
    f.write("""</body>
</html>""")

if len(sys.argv) < 3:
    print "Usage: %s PARTS_LIST PARTS_DB OUTFILE" % (os.path.basename(sys.argv[0]))
    print "Where:"
    print "	- PARTS_LIST is the EAGLE parts list"
    print "	- PARTS_DB is the SR parts database"
    print "	- OUTFILE is the output HTML file"
    sys.exit(1)

[parts_fname, db_fname, out_fname] = sys.argv[1:4]

parts = parts_parser.EagleParts(parts_fname)
lib = parts_db.Db(db_fname)
outf = open( out_fname, "w" )

html_header(outf)
for id in parts.keys():
    sr_id = parts[id]

    if not lib.has_key(sr_id):
        continue

    outf.write("<tr>")
    for x in [ id, lib[sr_id]["description"], lib[sr_id]["supplier"], lib[sr_id]["order-number"] ]:
        outf.write("<td>%s</td>" % x)
    outf.write("</tr>")

html_footer(outf)
