from __future__ import print_function


def command(args):
    import sys
    import os
    import re

    assetname = args.assetname

    if os.path.isdir(assetname):
        assetname = os.path.join(assetname, "info")
        if not os.path.isfile(assetname):
            print("Cannot find 'info' file for assembly")
            sys.exit(1)

    os.rename(assetname, "{}-tmp".format(assetname))

    try:
        new = open(assetname, "w")
        old = open("{}-tmp".format(assetname))

        for line in old:
            revmatch = re.match("^[ ]*revision\\s*:\\s*([0-9]+)", line)
            if revmatch:
                rev = int(revmatch.group(1))
                line = re.sub("([^0-9]*)[0-9]*([^0-9]*)", "\\g<1>{}\\g<2>"
                              .format(rev + 1), line)

            new.write(line)
    except:
        print("Failed to update revision number:", sys.exc_info()[0])
        os.rename("{}-tmp".format(assetname), assetname)
    else:
        os.remove("{}-tmp".format(assetname))
        old.close()
        new.close()


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'inv-touch', help='Increment revision of an asset.')
    parser.add_argument('assetname', help='The asset name.')
    parser.set_defaults(func=command)
