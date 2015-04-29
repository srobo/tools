from __future__ import print_function


def get_duplicates(items):
    import collections

    return [x for x, y in collections.Counter(items).items() if y > 1]


def command(args):
    from sr.tools.inventory.inventory import get_inventory

    inventory = get_inventory()

    errors = 0

    # check for duplicate asset codes
    duplicate_asset_codes = get_duplicates(inventory.asset_codes)
    if duplicate_asset_codes:
        print('There are duplicate asset codes:',
              ', '.join(duplicate_asset_codes))
        errors += 1

    if errors == 0:
        print('No problems found. :)')


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-validate',
                                   help='Check the state of the inventory.')
    parser.set_defaults(func=command)
