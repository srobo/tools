from __future__ import print_function


def command(args):
    import sr.tools.bom.bom as bom
    import sr.tools.bom.parts_db as parts_db

    db = parts_db.get_db()
    m = bom.MultiBoardBom(db)
    m.load_boards_args(args.arg)

    m.prime_cache()

    # Group the parts by distributor:
    # Keys of ths dictionary are the distributor
    dist = {}

    for srcode, pg in m.items():
        if srcode == "sr-nothing":
            continue

        supplier = pg.part["supplier"]
        dist.setdefault(supplier, []).append(pg)

    for d, partgroups in dist.items():
        print("Distributor: %s" % d)
        for pg in partgroups:
            n = pg.order_num()
            if n is None:
                print("FAIL :-(")
            else:
                if d == "farnell":
                    print("%s, %i" % (pg.part["order-number"], pg.order_num()))
                else:
                    print(" - %i * %s" %
                          (pg.order_num(), pg.part["order-number"]))

    print("Total Price:", m.get_price())


def add_subparser(subparsers):
    parser = subparsers.add_parser('create-order',
                                   help="Generate the data to stick into a "
                                        "supplier's website")
    parser.add_argument('arg', nargs='+', help="""DIR -N SCHEMATIC1 -M SCHEMATIC2 ...
Where N and M are multipliers for the number of boards

create-order generates the data to stick into a supplier's
website, or send to a supplier (if they don't support such
things), for an order made up of the given numbers of
schematics.""")
    parser.set_defaults(func=command)
