import argparse
import importlib
import sys
import traceback

import pkg_resources

from sr.tools import __description__
from sr.tools.inventory.inventory import NotAnInventoryError

# make sure to update this with new tools if they are created
__all__ = [
    'cam_serial',
    'check_my_git',
    'clone_team',
    'clone',
    'comp_calculate_league_matches',
    'create_bom',
    'create_order',
    'digikey',
    'export_gerber',
    'farnell',
    'geda_hierpcb',
    'got_mcf',
    'help',
    'ide_list_repos',
    'ide_list_teams',
    'ide_version',
    'inv_edit',
    'inv_findpart',
    'inv_history',
    'inv_list_assy_templates',
    'inv_list_templates',
    'inv_mv',
    'inv_new_asset',
    'inv_new_group',
    'inv_query',
    'inv_set_attr',
    'inv_show_parent',
    'inv_show',
    'inv_sync_asset',
    'inv_touch',
    'inv_validate',
    'list_commands',
    'mcv4b_part_code',
    'mouser',
    'pcb_lint',
    'pcb_to_thou',
    'price_graph',
    'repolist',
    'rs',
    'schedule_knockout',
    'sd_serial',
    'stockcheck',
    'symbol_correct',
    'update',
    'usb_key_serial',
]


def get_version():
    version = pkg_resources.get_distribution('sr.tools').version
    return "Student Robotics Tools {} (Python {}.{}.{})".format(
        version,
        *sys.version_info[0:3],
    )


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '--version',
        '-v',
        help='Show version of the tools.',
        action='version',
        version=get_version(),
    )

    subparsers = parser.add_subparsers()
    for command in __all__:
        name = f'{__name__}.{command}'
        importlib.import_module(name).add_subparser(subparsers)

    args = parser.parse_args()

    if 'func' in args:
        try:
            args.func(args)
        except ImportError as e:
            try:
                name = e.name
            except AttributeError:
                name = str(e)

            print(
                "Please install the '{name}' module to use this tool.".format(
                    name=name,
                ),
                file=sys.stderr,
            )
            sys.exit(1)
        except NotAnInventoryError as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)
            sys.exit(3)
    else:
        parser.print_help()
