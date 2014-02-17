"Library for accessing the budget files"
import yaml, os, sys, logging
import collections
from decimal import ( Decimal as D, ROUND_CEILING, ROUND_FLOOR,
                      ROUND_UP )
import math
import runpy
import sys, tempfile
from subprocess import ( check_call, check_output,
                         CalledProcessError )
from tempfile import NamedTemporaryFile
import tokenize
from StringIO import StringIO

# Spending against a budget line is allowed to go over its value by
# this factor
FUDGE_FACTOR = D("1.1")

try:
    from yaml import CLoader as YAML_Loader
except ImportError:
    from yaml import Loader as YAML_Loader

def dec_ceil(d):
    return d.to_integral_exact( ROUND_CEILING )

def dec_floor(d):
    return d.to_integral_exact( ROUND_FLOOR )

def py_translate_to_decimals(s):
    "Translate any literal floats in the given source into decimals"

    # Parse numbers in the string as Decimals
    # based on example from http://docs.python.org/2.7/library/tokenize.html
    result = []
    g = tokenize.generate_tokens(StringIO(s).readline)
    for toknum, tokval, _, _, _  in g:
        if toknum == tokenize.NUMBER and '.' in tokval:
            result.extend([
                (tokenize.NAME, 'Decimal'),
                (tokenize.OP, '('),
                (tokenize.STRING, repr(tokval)),
                (tokenize.OP, ')')
            ])
        else:
            result.append((toknum, tokval))

    # Turn it back into python
    return tokenize.untokenize(result)

class BudgetItem(object):
    def __init__(self, name, fname, conf ):
        self.fname = fname
        self.conf = conf
        y = yaml.load( open(fname, "r"), Loader = YAML_Loader )

        if False in [x in y for x in ["cost", "summary", "description"]]:
            print >>sys.stderr, "Error: %s does not match schema." % fname
            exit(1)

        self.name = name
        self.summary = y["summary"]
        self.description = y["description"]

        if "closed" in y:
            self.closed = y["closed"]
        else:
            self.closed = False

        if "consumable" in y:
            self.consumable = y["consumable"]
        else:
            self.consumable = None

        self.cost = self._parse_cost( y["cost"], conf )

    def _parse_cost(self, s, conf):
        "Parse the cost string"

        s = py_translate_to_decimals(s)
        cost = eval( s,
                     {"Decimal": D,
                      "ceiling": dec_ceil,
                      "floor": dec_floor},
                     conf.vars )

        if type(cost) is int:
            cost = D(cost)

        # Round the result up to the nearest penny
        cost = cost.quantize( D("0.01"), rounding = ROUND_UP )

        return cost

class InvalidPath(Exception):
    pass

class BudgetTree(object):
    "Container for the BudgetItems and BudgetTrees below a certain point"
    def __init__(self, name):
        self.children = {}
        self.name = name

    def add_child(self, child):
        if isinstance(child, BudgetTree):
            self.children[ child.name ] = child
        elif isinstance(child, BudgetItem):
            self.children[ os.path.basename(child.name) ] = child
        else:
            raise Exception("Attempted to add unsupported object type to BudgetTree")

    def total(self):
        "Sum all children"
        t = D(0)
        for ent in self.children.values():
            if isinstance(ent, BudgetTree):
                t += ent.total()
            else:
                t += ent.cost
        return t

    def walk(self):
        "Walk through all the BudgetItems of the this tree"
        for c in self.children.values():
            if isinstance(c, BudgetItem):
                yield c
            elif isinstance(c, BudgetTree):
                for e in c.walk():
                    yield e

    def path(self, path):
        "Return the object at the given path relative to this one"
        pos = self
        for s in path.split("/"):
            try:
                pos = pos.children[s]
            except KeyError:
                raise InvalidPath( "'%s' has no child node '%s'" % ( pos.name, s ) )
        return pos

    def draw(self, fd = sys.stdout, space = "  ", prefix = "" ):
        "Draw a text-representation of the tree"

        print >>fd, "{prefix}--{name} ({cost})".format(prefix = prefix,
                                                      name = os.path.basename(self.name),
                                                      cost = self.total() )

        for n, c in enumerate(self.children.values()):
            child_prefix = prefix + space

            if isinstance(c, BudgetItem):
                if n == len(self.children)-1:
                    child_prefix += "+"
                else:
                    child_prefix += "|"

                print >>fd, "{prefix}--{name} ({cost})".format(prefix = child_prefix,
                                                              name = os.path.basename(c.name),
                                                              cost = c.cost )

            elif isinstance(c, BudgetTree):
                child_prefix = prefix + space

                if n == len(self.children)-1:
                    child_prefix += " "
                else:
                    child_prefix += "|"

                c.draw( fd = fd, prefix = child_prefix )

class BudgetConfig(object):
    def __init__(self, root):
        pypath = os.path.join( root, "config.py" )
        yamlpath = os.path.join( root, "config.yaml" )

        if os.path.exists( pypath ):
            self._load_from_py( pypath )
            self.path = pypath
        elif os.path.exists( yamlpath ):
            self._load_from_yaml( yamlpath )
            self.path = yamlpath
        else:
            raise Exception("No config file found")

    def _load_from_py(self, fname):
        conf = runpy.run_path( fname )

        # Variables that are part of the normal running environment
        nullset = set( runpy.run_path( "/dev/null" ).keys() )

        # Remove vars that are part of the normal running env
        for name in nullset:
            if name in conf:
                conf.pop(name)

        self.vars = conf

        for vname in self.vars.keys():
            val = self.vars[vname]
            if type(val) not in [int, D, float]:
                self.vars.pop(vname)

    def _load_from_yaml(self, fname):
        # Munge the old yaml file into a python file

        def dict_constructor(loader, node):
            return collections.OrderedDict(loader.construct_pairs(node))

        # Give me ordered dictionaries back
        yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                             dict_constructor)

        # Use the python loader to make ordered dicts work
        y = yaml.load(open(fname, "r"))

        with NamedTemporaryFile() as f:
            print >>f, "from math import ceil as ceiling, floor"

            for vname, val in y["vars"].iteritems():
                print >>f, "{0} = {1}".format( vname, val )

            f.flush()
            self._load_from_py(f.name)

def load_budget(root):
    root = os.path.abspath(root)
    funds_in_path = os.path.join( root, "funds-in.yaml" )
    conf = BudgetConfig( root )
    budget = []
    tree = BudgetTree("sr")

    for dirpath, dirnames, filenames in os.walk(root):
        for d in [".git", ".meta"]:
            try:
                dirnames.remove(d)
            except ValueError:
                "Those directories will not always be there"
                pass

        for fname in filenames:
            fullp = os.path.abspath( os.path.join(dirpath, fname) )
            if fullp in [conf.path, funds_in_path]:
                "These files are yaml files, but not budget items"
                continue

            if fname[-5:] != ".yaml":
                continue

            name = fullp[len(root)+1:-5]

            r = tree
            for d in name.split("/")[:-1]:
                if d not in r.children:
                    r.add_child( BudgetTree(d) )

                r = r.children[d]

            r.add_child( BudgetItem(name, fullp, conf) )
    return tree

class TmpBudgetExport(object):
    def __init__(self, root, rev):
        self.rev = rev
        self.tmpdir = tempfile.mkdtemp()

        self._export( root, rev, self.tmpdir )
        self.btree = load_budget( self.tmpdir )

    def _export(self, root, rev, path):
        check_call( "git archive {0} | tar -x -C {1}".format( rev, path ),
                    cwd = root,
                    shell = True )

    def __del__(self):
        import shutil
        shutil.rmtree(self.tmpdir)

def load_budget_rev( root, rev, keep_around = False ):
    "Load a named revision of the budget"
    t = TmpBudgetExport( root, rev )

    if not keep_around:
        return t.btree

    return t.btree, t

class NotBudgetRepo(Exception):
    pass

def find_root( path = os.getcwd() ):
    """Find the root directory of the budget repository

    Checks that the repository is budget.git too

    Arguments:
    path -- if provided is a path within the budget.git repository
            (defaults to working directory)"""

    try:
        "Check that we're in budget.git"

        with open("/dev/null", "w") as n:
            check_call( ["git", "rev-list",
                         # This is the first commit of spending.git
                         "c7e8a3bdc82ad244ed302bf9a7f4934e0ca83292" ],
                        cwd = path,
                        stdout = n,
                        stderr = n )
    except CalledProcessError:
        "It's not the spending repository"
        raise NotBudgetRepo

    root = check_output( [ "git", "rev-parse", "--show-toplevel" ],
                         cwd = path )

    # Remove newline
    return root[0:-1]
