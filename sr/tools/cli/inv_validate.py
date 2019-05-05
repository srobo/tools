from __future__ import print_function

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def get_duplicates(items):
    import collections

    return [x for x, y in collections.Counter(items).items() if y > 1]


@check
def check_no_duplicates(inventory):
    duplicate_asset_codes = get_duplicates(inventory.asset_codes)
    if duplicate_asset_codes:
        codes_str = ", ".join(duplicate_asset_codes)
        return "There are duplicate asset codes: " + codes_str


@check
def check_assets_are_valid(inventory):
    from sr.tools.inventory.assetcode import is_valid

    invalid_asset_codes = [
        code for code in inventory.asset_codes if not is_valid(code)
    ]

    if invalid_asset_codes:
        codes_str = ", ".join(invalid_asset_codes)
        return "There are invalid asset codes: " + codes_str


def command(args):
    from sr.tools.inventory.inventory import get_inventory

    inventory = get_inventory()

    errors = 0
    for check_fn in CHECKS:
        message = check_fn(inventory)
        if message:
            print(message)
            errors += 1

    if errors == 0:
        print('No problems found. :)')


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-validate',
                                   help='Check the state of the inventory.')
    parser.set_defaults(func=command)
