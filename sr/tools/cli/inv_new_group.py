from __future__ import print_function


def command(args):
    import argparse
    import os

    import yaml

    from sr.tools.environment import open_editor
    from sr.tools.inventory.inventory import get_inventory
    from sr.tools.cli import inv_new_asset

    dirname = args.dirname

    inventory = get_inventory()
    gitdir = inventory.root_path

    # Find out if there's a template for the 'info' file
    templatefn = os.path.join(gitdir, ".meta", "assemblies", dirname)
    if not os.path.isfile(templatefn):
        templatefn = os.path.join(gitdir, ".meta", "assemblies", "default")

    userno = inventory.current_user_number
    assetcd = inventory.get_next_asset_code(userno)

    groupname = "%s-sr%s" % (dirname, assetcd)

    if os.path.isdir(dirname):
        os.rename(dirname, groupname)
    else:
        os.mkdir(groupname)

    print("Created new assembly with name \"%s\"" % groupname)

    # Copy the group template to the group dir
    # Insert the asset code into the file while we're at it
    templatefile = open(templatefn)
    assetfile = open(os.path.join(groupname, "info"), "w")

    for line in templatefile:
        assetfile.write(line.replace("[ASSET_CODE]", assetcd))

    templatefile.close()
    assetfile.close()

    if args.start_editor:
        open_editor(os.path.join(groupname, "info"))

    if args.create_all:
        assy_data = yaml.load(open(templatefn))
        if "elements" in assy_data:
            os.chdir(groupname)
            for element in assy_data["elements"]:
                other_args = argparse.Namespace()
                other_args.assetname = element
                other_args.start_editor = args.start_editor
                inv_new_asset.command(other_args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-new-group',
                                   help="Promote a directory to a tracked "
                                        "assembly.")
    parser.add_argument("-a", "--all", action="store_true", default=False,
                        dest="create_all",
                        help="Create all of the elements of the assembly too. "
                             "This should only be used when initially adding "
                             "a whole assembly to the inventory")
    parser.add_argument("-e", "--editor", action="store_true", default=False,
                        dest="start_editor",
                        help="Open up the newly created assembly 'info' file "
                             "in $EDITOR. If the --all option is used then "
                             "also open the editor for each asset created.")
    parser.add_argument("dirname", metavar="DIR",
                        help="The directory to promote to a tracked assembly. "
                             "If it does not exist it will be created.")
    parser.set_defaults(func=command)
