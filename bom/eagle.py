"""Routines for extracting information from EAGLE schematics
You probably always want to import schem instead of this."""
import os, subprocess, tempfile

def file_is_eagle(f):
    """Return true if the file is an EAGLE file"""
    f.seek(0)
    b = f.read(2)

    # The first two bytes of eagle files seem either be 0x10 0x80 or 0x10 0x00
    if ord(b[0]) == 0x10 and (ord(b[1]) == 0x80 or ord(b[1]) == 0x00):
        return True
    return False

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


