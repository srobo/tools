from __future__ import print_function


# Motorobards have FTDI ICs on them
FTDI_ID_VENDOR = '0403'  # Future Technology Devices International, Ltd
FTDI_ID_PRODUCT = '6001'  # FT232 USB-Serial (UART) IC

# Manufacturer/product details written to the FTDI IC's EEPROM
MCV4B_MANUFACTURER = 'Student Robotics'
MCV4B_PRODUCT = 'MCV4B'


def _has_attr(device, key, value):
    """
    Returns True if the udev Device has the attribute 'key' set to 'value'.
    """
    attrs = device.attributes
    return key in attrs.keys() and attrs[key] == value


id_vendor_match = lambda d: _has_attr(d, 'idVendor',     FTDI_ID_VENDOR)
id_product_match = lambda d: _has_attr(d, 'idProduct',    FTDI_ID_PRODUCT)
product_match = lambda d: _has_attr(d, 'product',      MCV4B_PRODUCT)
manufacturer_match = lambda d: _has_attr(d, 'manufacturer', MCV4B_MANUFACTURER)


def partcode_match(device):
    """
    Returns True if the udev Device has a valid SR partcode in its 'serial'
    attribute.
    """
    import re

    from sr.tools.inventory import assetcode

    if 'serial' not in device.attributes:
        return False

    ALPHA = "".join(assetcode.alphabet_lut)
    PARTCODE_RE = re.compile("sr([{0}]+)$".format(ALPHA), re.IGNORECASE)

    # does it look like a partcode?
    match = PARTCODE_RE.match(device.attributes['serial'])
    if not match:
        return False
    try:
        # is the partcode valid?
        assetcode.code_to_num(match.groups()[0])
        return True
    except:
        return False


def is_motorboard(device):
    """
    Returns True if all of the match conditions are met.
    """
    for matcher in (id_vendor_match, id_product_match,
                    product_match, manufacturer_match,
                    partcode_match):
        if not matcher(device):
            return False

    # OK, we're now *really* sure this is a MCv4b motorboard
    return True


def find_motorboards(context):
    """
    Returns a list of MCv4B motorboards that are *currently* plugged in.
    """
    return [dev for dev in context.list_devices() if is_motorboard(dev)]


def wait_for_first_insertion(context):
    """
    Returns the *next* MCv4B motorboard to be plugged in.

    This function monitors udev additions (i.e. insertions), checking each as
    they happen.  The first device that looks like a motorboard is returned.
    """
    import pyudev

    monitor = pyudev.Monitor.from_netlink(context)
    for action, device in monitor:
        if action == 'add':
            if is_motorboard(device):
                return device


def command(args):
    import os

    import pyudev

    from sr.tools.inventory import query

    context = pyudev.Context()

    if args.wait:
        devices = [wait_for_first_insertion(context)]
    else:
        devices = find_motorboards(context)

    for device in devices:
        serial = device.attributes['serial']

        if args.output == "code":
            print(serial)
        else:
            os.chdir(args.inv_dir)
            res = query.query("code:{0}".format(serial))[0]

            if args.output == "path":
                print(res.path)


def add_subparser(subparsers):
    parser = subparsers.add_parser('mcv4b-part-code',
                                   help="Finds connected MCv4b motorboards by "
                                        "searching or waiting for insertion.  "
                                        "Two output formats are provided: "
                                        "'code' - just the SR part code; "
                                        "'path' - just the local "
                                        "inventory.git path (see --inv-dir)")
    parser.add_argument("--wait", action="store_true",
                        help="Wait for a MCv4b to be inserted instead of "
                             "searching")
    parser.add_argument("-o", "--output", type=str, default="code",
                        choices=["code", "path"],
                        help="Selects an output style (Default: code)")
    parser.add_argument("--inv-dir", type=str, default=".",
                        help="The root of the local inventory checkout, if "
                             "not pwd")
    parser.set_defaults(func=command)
