import hashlib, os, subprocess, re

from sr.tools.environment import get_cache_dir

def file_is_geda_pcb(f):
    """Return true if the file is a gEDA PCB file"""
    f.seek(0)

    # 'PCB[' will occur at the start of one of the first 20 or so lines
    for i in range(20):
        if re.search(r"^\s*PCB[ \t]*\[", f.readline()) is not None:
            return True
    return False

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
        cache_dir = get_cache_dir('bom', 'geda', 'bom')

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

class PCB:
    """Read in a gEDA PCB file"""

    def __init__(self, fname):
        self.fname = fname

    def __export_image(self, res, ofname):
        p = subprocess.Popen("""pcb -x png --as-shown --layer-stack "outline,component,silk" --dpi %s --outfile %s %s""" %
                             (res, ofname, self.fname), shell=True)
        p.communicate()
        p.wait()

    def __export_xy(self, ofname):
        p = subprocess.Popen("""pcb -x bom --xyfile %s %s""" %
                             (ofname, self.fname), shell=True)
        p.communicate()
        p.wait()

    def get_image(self, res):
        cache_dir = get_cache_dir('bom', 'geda', 'pcbimg')

        ab = os.path.abspath(self.fname)

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab + str(res))
        cfname = os.path.join(cache_dir, h.hexdigest())

        cache_good = False
        if os.path.exists(cfname):
            img_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > img_t:
                cache_good = True

        if not cache_good:
            self.__export_image(res, cfname)
        else:
            print("Using cached PCB image for %s" % os.path.basename(self.fname))

        f = open(cfname, "r")
        img = f.read()
        f.close()
        return img

    def get_xy(self):
        cache_dir = get_cache_dir('bom', 'geda', 'pcbxy')

        ab = os.path.abspath(self.fname)

        # Generate cache filename
        h = hashlib.sha1()
        h.update(ab)
        cfname = os.path.join(cache_dir, h.hexdigest())

        cache_good = False
        if os.path.exists(cfname):
            xy_t = os.path.getmtime(ab)
            cache_t = os.path.getmtime(cfname)

            if cache_t > xy_t:
                cache_good = True

        if not cache_good:
            self.__export_xy(cfname)
        else:
            print("Using cached PCB xy-data for %s" % os.path.basename(self.fname))

        f = open(cfname, "r")
        xy = f.read()
        f.close()
        return xy
