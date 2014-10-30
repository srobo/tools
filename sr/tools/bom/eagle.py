"""Routines for extracting information from EAGLE schematics
You probably always want to import schem instead of this."""
import os, subprocess, hashlib

def file_is_eagle(f):
    """Return true if the file is an EAGLE file"""
    f.seek(0)
    b = f.read(2)

    # The first two bytes of eagle files seem either be 0x10 0x80 or 0x10 0x00
    try:
        if ord(b[0]) == 0x10 and (ord(b[1]) == 0x80 or ord(b[1]) == 0x00):
            return True
    except:
        pass
    return False

def file_version(fname):
    """Get the eagle version of the given file.
    Returns a tuple containing the major and minor versions."""
    f = open(fname, "r")

    f.seek(8)
    b = f.read(2)
    return (ord(b[0]), ord(b[1]))

class EagleSchem(dict):
    """Reads in EAGLE file.
    Parts in file can be accessed like dictionary."""

    def __init__(self, fname):
        """Load the given file.  Grab the parts list."""
        self.fname = fname
        self.__load_bom_cached()

    def __load_bom_cached(self):
        "Load the BOM from cache if possible."
        cache_dir = os.path.expanduser( "~/.sr/cache/eagle_bom" )
        if not os.path.exists( cache_dir ):
            os.makedirs( cache_dir )

        ab = os.path.abspath( self.fname )

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab)
        cfname = os.path.join( cache_dir, h.hexdigest() )

        cache_good = False
        if os.path.exists( cfname ):
            # Discover if the cache is still valid
            schem_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > schem_t:
                "Cache is good"
                cache_good = True

        if not cache_good:
            self.__export_bom(cfname)
        else:
            print("Using cached BOM for %s." % os.path.basename(self.fname))

        self.__parse_bom_fname( cfname )

    def __parse_bom_fname(self, fname):
        f = open( fname, "r" )

        # Skip and check EAGLE header
        for i in range(8):
            l = f.readline()
            # line 5 starts with "EAGLE" in EAGLE parts lists.
            if i == 4 and l[0:5] != "EAGLE":
                raise Exception("Parts list '%s' is not an EAGLE parts list" % self.fname)

        for line in f:
            fields = line.split()

            value = fields[1].strip().lower() # e.g. sr-r-10k
            id = fields[0].strip().upper() # e.g. R1

            self[id] = value

        f.close()

    def __export_bom(self, out_fname):
        p = subprocess.Popen( """sr export_eagle_bom "%s" "%s" """ % (self.fname, out_fname),
                              shell = True )
        p.communicate()
        p.wait()
