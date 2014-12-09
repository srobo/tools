from __future__ import print_function


def command(args):
    import os
    import sys

    from sr.tools.environment import open_editor
    from sr.tools.inventory.inventory import find_top_level_dir

    # Check we're being run in the inventory repo
    gitdir = find_top_level_dir()
    if not gitdir:
        print("This command must be run in the inventory git repository.")
        sys.exit(2)

    for assetfn in args.assetfnames:
        assetname = assetfn[:assetfn.find("-sr")]
        assetcd = assetfn[assetfn.find("-sr") + 3:]
        # Check that a template for the asset exists
        templatefn = os.path.join(gitdir, ".meta", "parts", assetname)
        if not os.path.isfile(templatefn):
            print("A template for the asset \"%s\" could not be found. "
                  "Skipping." % assetname)
            continue

        templatefile = open(templatefn)
        assetfile = open(assetfn, "w")

        for line in templatefile:
            assetfile.write(line.replace("[ASSET_CODE]", assetcd))

        templatefile.close()
        assetfile.close()

        if args.start_editor:
            open_editor(assetfn)


def add_subparser(subparsers):
    parser = subparsers.add_parser('inv-sync-asset',
                                   help="Replace the contents of an asset "
                                        "file with the contents of its "
                                        "corresponding template. WARNING: "
                                        "This command will completely "
                                        "overwrite an asset file, this "
                                        "includes the 'labelled' field.")
    parser.add_argument("-e", "--editor", action="store_true", default=False,
                        dest="start_editor",
                        help="Opens up the modified asset file in $EDITOR")
    parser.add_argument("assetfnames", metavar="ASSET", nargs="+",
                        help="The name of an asset to synchronise with the "
                             "template.")
    parser.set_defaults(func=command)
