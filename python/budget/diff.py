"Functions for diffing BudgetTrees"
import budget
import sys, subprocess, tempfile, shutil
from subprocess import check_call

class AddedItem(object):
    def __init__(self, a):
        self.a = a

class RemovedItem(object):
    def __init__(self, a):
        self.a = a

class ChangedItem(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

def _item_dict( tree ):
    items = {}
    for i in tree.walk():
        items[i.name] = i

    return items

def diff_trees( a, b ):
    a_items = _item_dict(a)
    b_items = _item_dict(b)

    # Remove items from this list as we find them
    # it'll eventually have things in it that aren't in A
    added = list( b_items.values() )

    changes = []

    for ai in a_items.values():

        if ai.name in b_items:
            # Features in both trees
            bi = b_items[ai.name]
            added.remove(bi)

            if bi.cost != ai.cost:
                "Changed value"
                changes.append( ChangedItem( ai, bi ) )

        else:
            "It's been removed"
            changes.append( RemovedItem( ai ) )

    for i in added:
        changes.append( AddedItem( i ) )

    return changes

def incr_tree( changes ):
    "Convert a list of changes into a tree"

    tree = budget.BudgetTree("sr")

    for c in changes:
        item = None

        if isinstance( c, AddedItem):
            item = c.a

        elif isinstance( c, ChangedItem ):
            # Only pay attention if the cost increased
            if c.a.cost >= c.b.cost:
                continue

            # Craft a new item that only describes the increase in cost
            item = budget.BudgetItem( c.a.name,
                                      c.a.fname,
                                      c.a.conf )
            item.cost = c.b.cost - c.a.cost

        else:
            continue

        r = tree

        for d in item.name.split("/")[:-1]:
            if d not in r.children:
                r.add_child( budget.BudgetTree(d) )

            r = r.children[d]

        r.add_child( item )

    return tree
