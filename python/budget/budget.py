"Library for accessing the budget files"
import yaml, sympy, os, sys, logging
from decimal import Decimal as D
import sys, tempfile
from subprocess import check_call

class BudgetItem(object):
    def __init__(self, name, fname, conf ):
        self.fname = fname
        self.conf = conf
        y = yaml.load( open(fname, "r") )

        if False in [x in y for x in ["cost", "summary", "description"]]:
            print >>sys.stderr, "Error: %s does not match schema." % fname
            exit(1)

        self.name = name
        self.summary = y["summary"]
        self.description = y["description"]

        if "consumable" in y:
            self.consumable = y["consumable"]
        else:
            self.consumable = None

        c = sympy.S( y["cost"] )
        self.cost = D( "%.2f" % c.evalf( subs = conf.vars ) )

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
                raise Exception( "'%s' has no child node '%s'" % ( pos.name, s ) )
        return pos

class BudgetConfig(object):
    def __init__(self, fname):
        y = yaml.load( open(fname, "r") )

        if "vars" not in y:
            raise Exception("No variables declaration section in config")
        self.vars = y["vars"]

        # Perform substitution of config variables.
        # This allows something like the following to work
        # cost = thing; thing = a*2; a = b+2; b = 5
        for var in self.vars:
            # Have to repeat this until there's nothing left to substitute
            # Limit the number of iterations in case of recursion
            for i in range(0,20):
                self.vars[var] = sympy.S(self.vars[var]).subs(self.vars).evalf()

def load_budget(root):
    root = os.path.abspath(root)
    config_path = os.path.join( root, "config.yaml" )
    funds_in_path = os.path.join( root, "funds-in.yaml" )
    conf = BudgetConfig( config_path )
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
            if fullp in [config_path, funds_in_path]:
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

def load_budget_rev( root, rev ):
    "Load a named revision of the budget"
    t = TmpBudgetExport( root, rev )
    return t.btree
