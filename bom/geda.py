import hashlib, os, subprocess

class GSchem(dict):
    """Reads in gEDA file"""

    def __init__(self, fname):
        self.fname = fname
        self.__load_bom()

    def __export_bom(self, ofname):
        p = subprocess.Popen( """gnetlist -g partslist1 -o %s %s""" % (ofname, self.fname),
                              shell = True )
        p.communicate()
        p.wait()

    def __load_bom(self):
        cache_dir = os.path.expanduser("~/.sr/cache/geda_bom")
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
            print "Using cached BOM for %s." % os.path.basename(self.fname)
        
        self.__parse_bom_fname( cfname )

    def __parse_bom_fname( self, fname ):
        f = open( fname, "r" )

        # Skip the first two lines
        f.readline()
        f.readline()

        for line in f:
            if line[0] == ".":
                "Ignore lines beginning with '.'"
                continue

            fields = line.split()

            value = fields[2].strip().lower()
            id = fields[0].strip().upper()

            self[id] = value

        f.close()
