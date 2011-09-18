"API for the SR inventory"
import os, sys, re, yaml
import assetcode, codecs

RE_GROUP = re.compile( "^(.+-assy)-sr([%s]+)$" % "".join(assetcode.alphabet_lut) )
RE_PART = re.compile( "^(.+)-sr([%s]+)$" % "".join(assetcode.alphabet_lut) )

def should_ignore(path):
    "Return True if the path should be ignored"
    if path[0] == ".":
        return True

    if path[-1] == "~":
        return True

    return False

class Item(object):
    "An item in the inventory"
    def __init__(self, path):
        self.path = path
        m = RE_PART.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load data from yaml file
        self.info = yaml.load( codecs.open(path, "r", encoding="utf-8") )

        # Verify that assetcode matches filename
        if self.info["assetcode"] != self.code:
            print >>sys.stderr, "Code in asset filename does not match contents of file:"
            print >>sys.stderr, "\t code in filename: '%s'" % self.code
            print >>sys.stderr, "\t code in contents: '%s'" % self.info["assetcode"]
            print >>sys.stderr, "\n\tOffending file:", self.path
            exit(1)

        # The mandatory properties
        self.labelled = self.info["labelled"]
        self.description = self.info["description"]
        self.value = self.info["value"]
        self.condition = self.info["condition"]

class ItemTree(object):
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = path
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
                i = Item(p)
                self.children[i.code] = i

            elif os.path.isdir(p):
                "Could either be a group or a collection"

                if RE_GROUP.match(p) != None:
                    a = ItemGroup(p)
                    self.children[a.code] = a
                else:
                    t = ItemTree(p)
                    self.children[t.name] = t

    def walk(self):
        for child in self.children.values():
            if hasattr(child, "walk"):
                for c in child.walk():
                    yield c

            if hasattr(child, "code"):
                yield child

class ItemGroup(ItemTree):
    "A group of items"
    def __init__(self, path):
        ItemTree.__init__(self, path)

        m = RE_GROUP.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load info from 'info' file
        self.info = yaml.load( codecs.open( os.path.join( path, "info" ),
                                            "r", encoding="utf-8") )

        if self.info["assetcode"] != self.code:
            print >>sys.stderr, "Code in group directory name does not match info file:"
            print >>sys.stderr, "\t code in directory name: '%s'" % self.code
            print >>sys.stderr, "\t           code in info: '%s'" % self.info["assetcode"]
            print >>sys.stderr, "\n\tOffending group:", self.path
            exit(1)

        self.description = self.info["description"]
        if "elements" in self.info:
            self.elements = self.info["elements"]
        else:
            self.elements = []

    def walk(self):
        for child in self.children.values():
            yield child

class Inventory(object):
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.root = ItemTree(rootpath)
