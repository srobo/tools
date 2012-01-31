"API for the SR inventory"
import os, sys, re, yaml
import assetcode, codecs
import cPickle, hashlib

CACHE_DIR = os.path.expanduser( "~/.sr/cache/inventory" )

RE_PART = re.compile( "^(.+)-sr([%s]+)$" % "".join(assetcode.alphabet_lut) )

def should_ignore(path):
    "Return True if the path should be ignored"
    if path[0] == ".":
        return True

    if path[-1] == "~":
        return True

    return False

def cached_yaml_load( path ):
    "Load the pickled YAML file from cache"
    path = os.path.abspath( path )

    ho = hashlib.sha256()
    ho.update( path )
    h = ho.hexdigest()

    if not os.path.exists( CACHE_DIR ):
        os.makedirs( CACHE_DIR )

    p = os.path.join( CACHE_DIR, h )

    if os.path.exists( p ):
        "Cache has file"
        if os.path.getmtime(p) >= os.path.getmtime(path):
            "Check that it's newer"
            return cPickle.load( open(p, "r") )

    y = yaml.load( codecs.open(path, "r", encoding="utf-8") )
    cPickle.dump(y, open(p, "w"))
    return y

class Item(object):
    "An item in the inventory"
    def __init__(self, path, parent = None):
        self.path = path
        self.parent = parent
        m = RE_PART.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load data from yaml file
        self.info = cached_yaml_load( path )

        # Verify that assetcode matches filename
        if self.info["assetcode"] != self.code:
            print >>sys.stderr, "Code in asset filename does not match contents of file:"
            print >>sys.stderr, "\t code in filename: '%s'" % self.code
            print >>sys.stderr, "\t code in contents: '%s'" % self.info["assetcode"]
            print >>sys.stderr, "\n\tOffending file:", self.path
            exit(1)

        # The mandatory properties
        mand = ["labelled", "description", "value", "condition"]

        for pname in mand:
            try:
                setattr( self, pname, self.info[pname] )
            except KeyError:
                raise Exception( "Part sr{0} is missing '{1}' property".format( self.code,
                                                                                pname ) )

class ItemTree(object):
    def __init__(self, path, parent = None):
        self.name = os.path.basename(path)
        self.path = path
        self.parent = parent
        self.children = {}
        self._find_children()

        self.parts = {}
        self.types = {}
        for i in self.walk():
            self.parts[i.code] = i

            if i.name not in self.types:
                self.types[i.name] = []
            self.types[i.name].append(i)

    def _find_children(self):
        for fname in os.listdir(self.path):
            if should_ignore(fname) or fname == "info":
                "Ignore dotfiles and group description files"
                continue

            p = os.path.join(self.path, fname)

            if os.path.isfile(p):
                "It's got to be an item"
                i = Item(p, parent = self)
                self.children[i.code] = i

            elif os.path.isdir(p):
                "Could either be a group or a collection"

                if RE_PART.match(p) != None:
                    a = ItemGroup(p, parent = self)
                    self.children[a.code] = a
                else:
                    t = ItemTree(p, parent = self)
                    self.children[t.name] = t

    def walk(self):
        for child in self.children.values():
            if hasattr(child, "walk"):
                for c in child.walk():
                    yield c

            if hasattr(child, "code"):
                yield child

    def resolve(self, path):
        "Resolve the given path into an object"

        if path[0] == "/":
            path = path[1:]

        pos = self
        for n in path.split("/"):
            pos = pos.children[n]

        return pos

class ItemGroup(ItemTree):
    "A group of items"
    def __init__(self, path, parent = None):
        ItemTree.__init__(self, path, parent = parent)

        m = RE_PART.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load info from 'info' file
        self.info = cached_yaml_load( os.path.join( path, "info" ) )

        if self.info["assetcode"] != self.code:
            print >>sys.stderr, "Code in group directory name does not match info file:"
            print >>sys.stderr, "\t code in directory name: '%s'" % self.code
            print >>sys.stderr, "\t           code in info: '%s'" % self.info["assetcode"]
            print >>sys.stderr, "\n\tOffending group:", self.path
            exit(1)

        self.description = self.info["description"]

        if "elements" not in self.info:
            raise Exception("Group %s lacks an elements field" % self.code)

        self.elements = self.info["elements"]

class Inventory(object):
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.root = ItemTree(rootpath)
