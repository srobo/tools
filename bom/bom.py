# Routines for extracting BOMs from schematics
import subprocess, tempfile, os, sys

EAGLE = 0
UNKNOWN = 1

PARTS_DB = os.path.expanduser("~/.sr/tools/bom/sr_component_lib")
if not os.path.exists( PARTS_DB ):
    print "Parts DB not found at \"%s\"" % PARTS_DB
    sys.exit(1)

def file_is_eagle(f):
    """Return true if the file is an EAGLE file"""
    f.seek(0)
    b = f.read(2)

    # The first two bytes of eagle files seem either be 0x10 0x80 or 0x10 0x00
    if ord(b[0]) == 0x10 and (ord(b[1]) == 0x80 or ord(b[1]) == 0x00):
        return True
    return False

def schem_type(fname):
    """Returns the type of file.
    At the moment it'll return EAGLE or UNKNOWN."""
    f = open( fname, "r" )

    if file_is_eagle(f):
        return EAGLE

    return UNKNOWN

class EagleSchem(dict):
    """Reads in EAGLE file.
    Parts in file can be accessed like dictionary."""

    def __init__(self, fname):
        """Load the given file.  Grab the parts list."""
        self.fname = fname
        self.__load_bom()

    def __load_bom(self):
        # Export the EAGLE BOM to a temporary file
        tmpf = tempfile.mkstemp()
        os.close(tmpf[0])
        tmpf = tmpf[1]

        self.__export_bom(tmpf)

        f = open( tmpf, "r" )

        # Skip and check EAGLE header
        for i in range(8):
            l = f.readline()
            # line 5 starts with "EAGLE" in EAGLE parts lists.
            if i == 4 and l[0:5] != "EAGLE":
                raise Exception, "Parts list '%s' is not an EAGLE parts list" % self.fname
    
        for line in f:
            fields = line.split()

            value = fields[1].strip().lower() # e.g. sr-r-10k
            id = fields[0].strip().upper() # e.g. R1
            
            self[id] = value

        f.close()
        os.remove(tmpf)

    def __export_bom(self, out_fname):
        p = subprocess.Popen( """sr export_eagle_bom "%s" "%s" """ % (self.fname, out_fname),
                              shell = True )
        p.communicate()
        p.wait()

def open_schem(fname):
    s = schem_type(fname)
    if s == EAGLE:
        return EagleSchem(fname)
    else:
        raise "We don't yet support exporting BOMs from non-EAGLE things"
