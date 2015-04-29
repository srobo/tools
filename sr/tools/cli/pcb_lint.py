from __future__ import print_function


def command(args):
    import sys

    import sr.tools.bom.schem as schem
    import sr.tools.bom.parts_db as parts_db

    SCHEMATIC = args.schematic

    lib = parts_db.get_db()
    parts = schem.open_schem(SCHEMATIC)

    error = 0
    found = 0

    # Erroneous parts (key is type)
    err_parts = {}

    for id in parts.keys():
        if parts[id] not in lib:
            err_parts.setdefault(parts[id], []).append(id)
            error += 1
        else:
            found += 1

    print("%i correct parts found." % found)

    if len(err_parts) > 0:
        print("The following %i parts are not in the SR parts database:" %
              error)

        for name, components in err_parts.items():
            print("\t'%s': %s" % (name, " ".join(components)))

        sys.exit(2)


def command_deprecated(args):
    import sys

    print("This is deprecated, please use 'pcb-lint' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('pcb_lint',
                                   help="Checks that all the parts in a PCB's "
                                        'schematic are in the SR database')
    parser.add_argument('schematic', help='The schematic to check.')
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('pcb-lint',
                                   help="Checks that all the parts in a PCB's "
                                        'schematic are in the SR database')
    parser.add_argument('schematic', help='The schematic to check.')
    parser.set_defaults(func=command)
