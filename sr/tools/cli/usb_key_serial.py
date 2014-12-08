from __future__ import print_function

import sys


def command(args):
    try:
        import pyudev
    except ImportError:
        print("Please install 'pyudev' to use this tool.", file=sys.stderr)
        sys.exit(1)


    con = pyudev.Context()

    for dev in con.list_devices(subsystem="usb", ID_DRIVE_THUMB="1"):
        print(dev["ID_SERIAL_SHORT"])


def add_subparser(subparsers):
    parser = subparsers.add_parser('usb-key-serial',
                                   help='Displays the serial number of '
                                        'connected USB keys')
    parser.set_defaults(func=command)
