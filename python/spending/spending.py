"Library for accessing the spending files"
import yaml, os, sys, datetime, budget
from decimal import Decimal as D

class Transaction(object):
    def __init__(self, name, date, fname):
        self.fname = fname
        y = yaml.load( open(fname, "r") )

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
            repopath = fullp[len(root)+1:-(len(fname)+1)]
            if repopath == "pending":
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
    bud = budget.load_budget("budget/")
    trans = group_trans_by_budget_line(load_transactions(root))
    
    for b in bud.walk():
        if b.name in trans:
            b.transactions = trans[b.name]
        else:
            b.transactions = []
    
    return bud
