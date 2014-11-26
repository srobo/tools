from __future__ import print_function

try:
    import pygit2
    PYGIT2_AVAILABLE = True
except ImportError:
    PYGIT2_AVAILABLE = False

import sr.tools.inventory as srinv


def walk_history(tree, repo):
    for entry in tree:
        yield entry

        o = repo[entry.oid]
        if isinstance(o, pygit2.Tree):
            #yield from walk_history(o, repo)
            pass


def history(args):
    partcode = srinv.normalise_partcode(args.partcode)
    repo = pygit2.Repository(args.inventory)
    inventory = srinv.Inventory(args.inventory)
    part = inventory.root.parts[partcode]

    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
        for entry in walk_history(commit.tree, repo):
            if partcode in entry.name:
                print(entry.name)


def add_subparsers(subparsers):
    if PYGIT2_AVAILABLE:
        parser_history = subparsers.add_parser('inv-history',
                                               help='History about a item.')
        parser_history.add_argument('partcode')
        parser_history.add_argument('--inventory', '-i', default='.',
                                    help='Location of the inventory.')
        parser_history.set_defaults(func=history)
