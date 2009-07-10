# Routines for extracting BOMs from schematics
import subprocess, tempfile, os, sys, parts_db, schem

PARTS_DB = os.path.expanduser("~/.sr/tools/bom/sr_component_lib")
if not os.path.exists( PARTS_DB ):
    print "Parts DB not found at \"%s\"" % PARTS_DB
    sys.exit(1)

STOCK_OUT = 0
STOCK_OK = 1
STOCK_UNKNOWN = 2

class PartGroup(list):
    """A set of parts
    One might call this a "BOM line" """
    def __init__(self, part, name, designators = [] ):
        list.__init__(self)

        for x in designators:
            self.append( (name, designators) )

        self.part = part
        self.name = name

    def stockcheck(self):
        """Check the distributor has enough parts in stock."""
        s = self.part.stockcheck()
        if s == None:
            return None

        if s < len(self):
            return False
        return True

class Bom(dict):
    """BOM object.
    Groups parts with the same srcode into PartGroups.
    Dictionary keys are sr codes."""
    def __init__(self, db, fname, name ):
        """fname is the schematic to load from.  
        db is the parts database object.
        name is the name to give the schematic."""
        dict.__init__(self)
        self.db = db
        self.name = name

        s = schem.open_schem(fname)

        for des,srcode in s.iteritems():
            if not self.has_key(srcode):
                self[srcode] = PartGroup( db[srcode], name )
            self[srcode].append((name,des))

    def stockcheck(self):
        """Check that all items in the schematic are in stock.
        Returns list of things that aren't in stock."""

        for pg in self.values():
            a = pg.stockcheck()

            if a == None:
                yield (STOCK_UNKNOWN, pg.part)
            elif not a:
                yield (STOCK_OUT, pg.part)
            else:
                yield (STOCK_OK, pg.part)
