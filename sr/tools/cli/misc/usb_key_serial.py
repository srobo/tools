from __future__ import print_function


def command(args):
    import pyudev

    con = pyudev.Context()

    for dev in con.list_devices(subsystem="usb", ID_DRIVE_THUMB="1"):
        print(dev["ID_SERIAL_SHORT"])


def add_subparser(subparsers):
    parser = subparsers.add_parser('usb-key-serial',
                                   help='Displays the serial number of '
                                        'connected USB keys')
    parser.set_defaults(func=command)
