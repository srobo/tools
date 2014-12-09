from __future__ import print_function

import sys

import sr.tools.inventory.inventory as inventory
import sr.tools.inventory.oldinv as oldinv
import sr.tools.inventory.query_parser as query_parser


def _get_inv():
    """Get the path to the inventory."""
    top = oldinv.gettoplevel()
    if top is None:
        print("Error: Must be run from within the inventory.", file=sys.stderr)
        exit(1)
    return inventory.Inventory(top).root


def query(query_str, inv=None):
    """Run a query on the inventory."""
    if inv is None:
        inv = _get_inv()
    tree = query_parser.search_tree(query_str)
    return tree.match(inv.parts.values())
