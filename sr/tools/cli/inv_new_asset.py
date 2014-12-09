from __future__ import print_function


def command(args):
    import os
    import sys

    from sr.tools.environment import open_editor
    from sr.tools.inventory.inventory import find_top_level_dir
    from sr.tools.inventory.oldinv import getusername, getusernumber, \
        getpartnumber
    import sr.tools.inventory.assetcode as assetcode

    assetname = args.assetname

    # Check we're being run in the inventory repo
    gitdir = find_top_level_dir()
    if not gitdir:
        print("This command must be run in the inventory git repository.")
        sys.exit(2)

    # Check that a template for the new asset exists
    templatefn = os.path.join(gitdir, ".meta", "parts", assetname)
    if not os.path.isfile(templatefn):
        print('A template for the asset "{}" could not be found. '
              'The default template will be used.'.format(assetname))
        templatefn = os.path.join(gitdir, ".meta", "parts", "default")

    # Get the git name/email of the user
    username = getusername()

    userno = getusernumber(gitdir, username)
    partno = getpartnumber(gitdir, userno)

    assetcd = assetcode.num_to_code(userno, partno)
    assetfn = "%s-sr%s" % (assetname, assetcd)

    print('Created new asset with name "{0}-\033[1msr{1}\033[0m"'
          .format(assetname, assetcd))

    # Copy the template to the actual asset file
    # Insert the asset code into the file while we're at it
    templatefile = open(templatefn)
    assetfile = open(assetfn, "w")

    for line in templatefile:
        assetfile.write(line.replace("[ASSET_CODE]", assetcd))

    templatefile.close()
    assetfile.close()

    if args.start_editor:
        open_editor(assetfn)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-new-asset',
                                   help="Create a new instance of an asset "
                                        "with a unique asset code.")
    parser.add_argument("-e", "--editor", action="store_true", default=False,
                        dest="start_editor",
                        help="Open up the newly created asset file in $EDITOR")
    parser.add_argument("assetname", metavar="ASSET",
                        help="The name of an asset template file in "
                             "/.meta/parts.")
    parser.set_defaults(func=command)
