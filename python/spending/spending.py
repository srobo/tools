"Library for accessing the spending files"
import yaml, os, sys, datetime, sr.budget as budget
from subprocess import check_output, check_call, CalledProcessError
from decimal import Decimal as D

try:
    from yaml import CLoader as YAML_Loader
except ImportError:
    from yaml import Loader as YAML_Loader

def num_constructor(loader, node):
    "Constructor for libyaml to translate numeric literals to Decimals"
    return D( node.value )

# Parse floats as decimals
YAML_Loader.add_constructor( "tag:yaml.org,2002:float",
                             num_constructor )

class Transaction(object):
    def __init__(self, name, date, fname):
        self.fname = fname
        y = yaml.load( open(fname, "r"), Loader = YAML_Loader )

        if False in [x in y for x in ["summary", "description", "budget",
                                      "cost", "trac"]]:
            print >>sys.stderr, "Error: %s does not match schema." % fname
            exit(1)

        self.name = name # Not unique
        self.date = date # None if pending
        self.summary = y["summary"]
        self.description = y["description"]
        self.budget = y["budget"]
        self.cost = D( "%.2f" % y["cost"] )
        self.trac = y["trac"]

        for prop in [ "cheque", "payee", "ackdate" ]:
            if prop in y:
                setattr( self, prop, y[prop] )
            else:
                setattr( self, prop, None )

        self.bank_transfer = "bank-transfer" in y and y["bank-transfer"]

        # Strip the '.yaml' off the end of the budget field if it's present
        if self.budget[-5:] == ".yaml":
            self.budget = self.budget[:-5]

def load_transactions(root):
    root = os.path.abspath(root)
    transactions = []

    for dirpath, dirnames, filenames in os.walk(root):
        try:
            dirnames.remove(".git")
            dirnames.remove("budget")
        except ValueError:
            "Those directories will not always be there"
            pass

        for fname in filenames:
            fullp = os.path.abspath( os.path.join(dirpath, fname) )

            if fname[-5:] != ".yaml":
                continue

            # The name of a transaction is not unique as multiple transactions
            # with the same file name can exist in the spending repository.
            name = fname[:-5]
            
            # The date of the transaction if it has been reconciled. None if
            # it's still pending.
            topdir = fullp[len(root)+1:fullp.find('/',len(root)+1)]
            repopath = fullp[len(root)+1:-(len(fname)+1)]
            if topdir == "pending":
                date = None
            else:
                try:
                    tmp = repopath.split("/")
                    date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                except:
                    print >>sys.stderr, "Unable to determine the date of the transaction %s" % fullp
                    exit(1)

            transactions.append( Transaction(name, date, fullp) )
    return transactions

def group_trans_by_budget_line(trans):
    transgrp = {}
    for t in trans:
        if t.budget in transgrp:
            transgrp[t.budget].append(t)
        else:
            transgrp[t.budget] = [t]
    return transgrp

def load_budget_with_spending(root):
    bud = budget.load_budget( os.path.join( root, "budget/" ) )
    trans = group_trans_by_budget_line(load_transactions(root))
    
    for b in bud.walk():
        if b.name in trans:
            b.transactions = trans[b.name]
        else:
            b.transactions = []
    
    return bud

class NotSpendingRepo(Exception):
    pass

def find_root( path = os.getcwd() ):
    """Find the root directory of the spending repository

    Checks that the repository is spending.git too

    Arguments:
    path -- if provided is a path within the spending.git repository
            (defaults to working directory)"""

    try:
        "Check that we're in spending.git"

        with open("/dev/null", "w") as n:
            check_call( ["git", "rev-list",
                         # This is the first commit of spending.git
                         "82ab25832fea63773e0f98f1e3a2a1424ed8af6f" ],
                        cwd = path,
                        stdout = n,
                        stderr = n )
    except CalledProcessError:
        "It's not the spending repository"
        raise NotSpendingRepo

    root = check_output( [ "git", "rev-parse", "--show-toplevel" ],
                         cwd = path )

    # Remove newline
    return root[0:-1]
