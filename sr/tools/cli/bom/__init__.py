from sr.tools.cli.bom import create_bom, create_order, digikey, \
                             export_gerber, farnell, mouser, pcb_lint, \
                             price_graph, rs, stockcheck


def add_subparsers(subparsers):
    create_bom.add_subparser(subparsers)
    create_order.add_subparser(subparsers)
    digikey.add_subparser(subparsers)
    export_gerber.add_subparser(subparsers)
    farnell.add_subparser(subparsers)
    mouser.add_subparser(subparsers)
    pcb_lint.add_subparser(subparsers)
    price_graph.add_subparser(subparsers)
    rs.add_subparser(subparsers)
    stockcheck.add_subparser(subparsers)
