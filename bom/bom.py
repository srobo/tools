# Routines for extracting BOMs from schematics
import subprocess, tempfile, os, sys, parts_db, schem

PARTS_DB = os.path.expanduser("~/.sr/tools/bom/sr_component_lib")
if not os.path.exists( PARTS_DB ):
    print "Parts DB not found at \"%s\"" % PARTS_DB
    sys.exit(1)


