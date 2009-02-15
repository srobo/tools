"""Parses EAGLE parts lists"""

class EagleParts(dict):
    """Board parts list.  Behaves like dictionary.  Reads in EAGLE parts lists."""
    def __init__(self, fname):
        """Load the parts list from the file with path fname"""

        f = open( fname, "r" )

        # Skip and check EAGLE header
        for i in range(8):
            l = f.readline()
            # line 5 starts with "EAGLE" in EAGLE parts lists.
            if i == 4 and l[0:5] != "EAGLE":
                raise Exception, "Parts list '%s' is not an EAGLE parts list" % fname
    
        for line in f:
            fields = line.split()

            value = fields[1].strip().lower() # e.g. sr-r-10k
            id = fields[0].strip().upper() # e.g. R1
            
            self[id] = value

