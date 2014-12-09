from __future__ import print_function


def command(args):
    from pylab import bar, yticks, subplots_adjust, show
    from numpy import arange

    import sr.tools.bom.bom as bom
    import sr.tools.bom.parts_db as parts_db

    db = parts_db.get_db()
    m = bom.MultiBoardBom(db)
    m.load_boards_args(args.arg)
    m.prime_cache()

    prices = []

    for srcode, pg in m.items():
        if srcode == "sr-nothing":
            continue

        prices.append((srcode, pg.get_price()))

    prices.sort(key=lambda x: x[1])

    bar(0, 0.8, bottom=range(0, len(prices)), width=[x[1] for x in prices],
        orientation='horizontal')

    yticks(arange(0, len(prices)) + 0.4, [x[0] for x in prices])

    subplots_adjust(left=0.35)

    show()


def add_subparser(subparsers):
    parser = subparsers.add_parser('price-graph',
                                   help="Create a price graph.")
    parser.add_argument('arg', nargs='+', help="""DIR -N SCHEMATIC1 -M SCHEMATIC2 ...
Where N and M are multipliers for the number of boards""")
    parser.set_defaults(func=command)
