from __future__ import print_function


def command(args):
    import os

    from sr.tools.environment import open_editor
    from sr.tools.inventory.inventory import get_inventory

    assetname = args.assetname

    inventory = get_inventory()
    gitdir = inventory.root_path

    # Check that a template for the new asset exists
    templatefn = os.path.join(gitdir, ".meta", "parts", assetname)
    if not os.path.isfile(templatefn):
        print('A template for the asset "{}" could not be found. '
              'The default template will be used.'.format(assetname))
        templatefn = os.path.join(gitdir, ".meta", "parts", "default")

    # Get the git name/email of the user
    userno = inventory.current_user_number
    assetcd = inventory.get_next_asset_code(userno)

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
