from __future__ import print_function


def command(args):
    import sys

    try:
        import pyudev
    except ImportError:
        print("Please install 'pyudev' to use this tool.", file=sys.stderr)
        sys.exit(1)


    con = pyudev.Context()

    for dev in con.list_devices(subsystem="mmc"):
        print(dev.attributes["serial"])


def add_subparser(subparsers):
    parser = subparsers.add_parser('sd-serial',
                                   help='Displays the serial number of '
                                        'connected mmc cards.')
    parser.set_defaults(func=command)
