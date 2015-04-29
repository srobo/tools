"""Routines for extracting information from schematics."""
import re

from sr.tools.bom import geda, parts_db


GSCHEM = 1
UNKNOWN = 2


def schem_type(fname):
    """
    Get the type of file.

    :returns: ``GSCHEM`` or ``UNKNOWN``
    """
    return GSCHEM


def open_schem(fname):
    """
    Open a schematics file.

    :returns: The parsed schematic as an object.
    :raises ValueError: If the file is not a gschem file.
    """
    s = schem_type(fname)
    if s == GSCHEM:
        schem = geda.GSchem(fname)
    else:
        raise ValueError("We don't yet support exporting BOMs from "
                         "gschem things.")

    # New items to add to the schematic
    new_items = {}
    # Items to remove from the schematic
    rem_keys = []

    # Expand all assemblies into their component parts:
    for des, srcode in schem.items():
        num = 1

        if srcode[0:len("sr-asm-")] == "sr-asm-":
            # TODO: Don't parse the Db again!
            db = parts_db.get_db()

            desc = db[srcode]["description"]

            for s in desc.split():
                if s == "+":
                    continue

                r = re.compile("([0-9]+)\(([^)]+)\)")
                m = r.match(s)
                if m:

                    quantity = int(m.group(1))
                    code = m.group(2)

                    for x in range(quantity):
                        newdes = "%s.%i" % (des, num)

                        new_items[newdes] = code
                        num = num + 1

            rem_keys.append(des)

    schem.update(new_items)
    for des in rem_keys:
        schem.pop(des)

    return schem
