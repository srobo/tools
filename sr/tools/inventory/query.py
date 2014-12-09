from __future__ import print_function

import sys

import sr.tools.inventory.inventory as inventory
import sr.tools.inventory.query_parser as query_parser


def query(query_str, inv=None):
    """Run a query on the inventory."""
    if inv is None:
        inv = inventory.get_inventory()

    tree = query_parser.search_tree(query_str)
    return tree.match(inv.root.parts.values())
