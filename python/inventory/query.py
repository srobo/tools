import inventory
import oldinv
import query_parser

def _get_inv():
    top = oldinv.gettoplevel()
    if top is None:
        print >>sys.stderr, "Error: Must be run from within the inventory."
        exit(1)
    return inventory.Inventory(top).root

def query(query_str):
    inv = _get_inv()
    tree = query_parser.search_tree(query_str)
    return tree.match(inv.parts.values())
