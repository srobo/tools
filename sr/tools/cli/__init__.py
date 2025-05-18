import argparse
import importlib
import sys
import traceback

from sr.tools import __description__, __version__
from sr.tools.inventory.inventory import NotAnInventoryError

# make sure to update this with new tools if they are created
__all__ = [
    'cam_serial',
    'check_my_git',
    'clone',
    'comp_calculate_league_matches',
    'help',
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
    'repolist',
    'schedule_knockout',
    'update',
]


def get_version():
    # importlib.metadata.version('sr.tools') only works with python >=3.10
    return "Student Robotics Tools {} (Python {}.{}.{})".format(
        __version__,
        *sys.version_info[0:3],
    )


def main(args=sys.argv):
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

    args = parser.parse_args(args=args[1:])

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
