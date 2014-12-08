from __future__ import print_function


# Vendor ID, Product ID
SR_CAMERA_IDS = [
    # The Logitech C500
    (0x046d, 0x0807),
    # The Logitech C270
    (0x046d, 0x0825)
]


def command(args):
    import pyudev

    con = pyudev.Context()

    for dev in con.list_devices(subsystem="video4linux"):
        usb_dev = dev.parent.parent
        assert usb_dev.subsystem == "usb"

        a = usb_dev.attributes
        ident = (int(a["idVendor"], 16),
                 int(a["idProduct"], 16))

        if ident not in SR_CAMERA_IDS:
            continue

        print(a["serial"])


def add_subparser(subparsers):
    parser = subparsers.add_parser('cam-serial',
                                   help='Displays the serial number of '
                                        'connected SR cameras')
    parser.set_defaults(func=command)
