"""Student Robotics parts database access library"""
import csv, farnell, rs, digikey, mouser, os, sys

PARTS_DB = os.path.expanduser("~/.sr/tools/bom/sr_component_lib")
if not os.path.exists( PARTS_DB ):
    print "Parts DB not found at \"%s\"" % PARTS_DB
    sys.exit(1)

def get_db():
    return Db(PARTS_DB)

class Part(dict):
    """Represents a part"""
    def __init__(self, d):
        """Initialise with a dict from the DB"""
        for k in d.keys():
            if isinstance(d[k], str):
                d[k] = d[k].strip()

        for k,v in d.iteritems():
            self[k] = v

        self.loaded = False

    def stockcheck(self):
        """Return how many of the product are in stock."""
        if not self.loaded:
            self.__load_data()

        return self.stock

    def get_price(self, num):
        "Get the unit price when buying num distributor units"
        if not self.loaded:
            self.__load_data()

        if self.stock == None:
            return None

        price = None
        for threshold, p in self.prices:
            if threshold >= num:
                return p
            price = p

        return price

    def get_dist_units(self):
        """Number of components per distributor unit"""
        if not self.loaded:
            self.__load_data()
        
        return self.dist_unit

    def get_min_order(self):
        if not self.loaded:
            self.__load_data()
        
        return self.min_order

    def get_increments(self):
        if not self.loaded:
            self.__load_data()
        
        return self.increments

    def get_url(self):
        if self["supplier"] == "farnell":
            return "https://xgoat.com/p/farnell/%s" % self["order-number"]
        if self["supplier"] == "rs":
            return "https://xgoat.com/p/rs/%s" % self["order-number"]
        if self["supplier"] == "digikey":
            return "https://xgoat.com/p/digikey/%s" % self["order-number"]

        return None

    def __load_data(self):
        o = None

        if self["supplier"] == "farnell":
            o = farnell.Item( self["order-number"] )
        elif self["supplier"] == "rs":
            o = rs.Item( self["order-number"] )
        elif self["supplier"] == "digikey":
            o = digikey.Item( self["order-number"] )
        elif self["supplier"] == "mouser":
            o = mouser.Item( self["order-number"] )
        else:
            self.stock = None
            return

        self.stock = o.avail
        self.min_order = o.min_order
        self.dist_unit = o.price_for
        self.increments = o.multi
        self.prices = o.prices

        self.loaded = True

class Db(dict):
    def __init__(self, fname):
        f = open(fname, "r")
        r = csv.DictReader(f)

        for line in r:
            # Discard commented out lines
            if line["sr-code"].strip()[0] == "#":
                continue

            part = Part(line)
            self[ part["sr-code"] ] = part
