from __future__ import print_function


def command(args):
    import argparse
    import pydoc
    import subprocess

    import sr.tools.inventory as srinv
    from sr.tools.inventory import get_inventory
    from sr.tools.inventory import normalise_partcode


    inv = get_inventory()

    partcode = normalise_partcode(args.partcode)
    part = inv.root.parts[partcode]

    pager_text = "Full path: " + part.path
    with open(part.info_path, 'r') as info_file:
        pager_text += info_file.read() + '\n'

    pager_text += "Log\n===\n"
    pager_text += subprocess.check_output(['git', '--no-pager', 'log', '--color',
                                          '--follow', '-C', '-M', part.path],
                                          universal_newlines=True)

    pydoc.pager(pager_text)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-show', help='Show the metadata of a given part, and its git history.')
    parser.add_argument('partcode', type=str, help="The part code to look up.")
    parser.set_defaults(func=command)
