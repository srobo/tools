"Functions for diffing BudgetTrees"
from sr.tools.budget import budget
import sys, subprocess, tempfile, shutil, os
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

    return sorted(changes, key=lambda change: change.a.name)

def changes_to_tree( changes ):
    "Convert a list of changes into a tree"

    tree = budget.BudgetTree("sr")

    for c in changes:
        item = None

        if isinstance( c, AddedItem):
            item = c.a

        elif isinstance( c, ChangedItem ):
            # Craft a new item that describes the change in cost
            item = budget.BudgetItem( c.a.name,
                                      c.a.fname,
                                      c.a.conf )
            item.cost = c.b.cost - c.a.cost

        elif isinstance( c, RemovedItem ):
            # Craft a new item that describes the reduction in cost

            item = budget.BudgetItem( c.a.name,
                                      c.a.fname,
                                      c.a.conf )
            item.cost *= -1

        else:
            raise Exception("Unsupported object type in change list")

        def fudge_parent(parents, name):
            "Fudge a directory name in because there were two..."
            name = "{0}.d".format( name )
            if name in parents[-1].children:
                res = parents[-1].children[name]
            else:
                res = budget.BudgetTree( name )
                parents[-1].add_child(res)

            return res

        r = tree
        parents = []

        for d in item.name.split("/")[:-1]:

            if not hasattr( r, "children" ):
                "It's not a directory -- add a directory at the same level with '.d' on the end"
                r = fudge_parent( parents, d )

            if d not in r.children:
                r.add_child( budget.BudgetTree(d) )

            parents.append(r)
            r = r.children[d]

        if not isinstance( r, budget.BudgetTree ):
            "Need to fudge a directory in"
            r = fudge_parent( parents, os.path.basename(r.name) )

        if os.path.basename(item.name) in r.children:
            raise Exception("Unsupported situation!")

        r.add_child( item )

    return tree
