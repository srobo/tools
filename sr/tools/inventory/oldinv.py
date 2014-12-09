"""Old API calls for the inventory."""

import os

from sr.tools.inventory import assetcode


def getpartnumbers(topd):
    """Recursively get a list of all part numbers."""
    parts = []

    for d in os.listdir(topd):
        if d in [".git", ".meta"]:
            continue

        path = os.path.join(topd, d)

        if os.path.isdir(path):
            parts.extend(getpartnumbers(path))
            try:
                acode = d[d.rindex("-sr") + 3:]
            except:
                continue
            parts.append(assetcode.code_to_num(acode))
        elif os.path.isfile(path):
            if path[-1] == "~":
                # ignore temporary files from editors
                continue

            fname = os.path.basename(path)
            try:
                acode = fname[fname.rindex("-sr") + 3:]
            except:
                continue
            parts.append(assetcode.code_to_num(acode))

    return parts


def getpartnumber(gitdir, userno):
    """Get the next available part number."""
    maxno = -1
    # Gather all part numbers from the inventory
    partnos = getpartnumbers(gitdir)
    for p in partnos:
        if p[0] == userno:
            maxno = max(maxno, p[1])
    return maxno + 1
