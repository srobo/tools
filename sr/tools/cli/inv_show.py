from __future__ import print_function


def command(args):
    import pydoc
    import subprocess

    from sr.tools.inventory import assetcode
    from sr.tools.inventory.inventory import get_inventory

    inv = get_inventory()

    partcode = assetcode.normalise(args.partcode)
    part = inv.root.parts[partcode]

    pager_text = "Full path: " + part.path + '\n'
    with open(part.info_path, 'r') as info_file:
        pager_text += info_file.read() + '\n'

    pager_text += "Log\n===\n"
    pager_text += subprocess.check_output(['git', '--no-pager', 'log',
                                           '--color', '--follow', '-C', '-M',
                                           part.path],
                                          universal_newlines=True)

    pydoc.pager(pager_text)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-show',
                                   help='Show the metadata of a given part, '
                                        'and its git history.')
    parser.add_argument('partcode', type=str, help="The part code to look up.")
    parser.set_defaults(func=command)
