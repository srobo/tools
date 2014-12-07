from sr.tools.cli.pcb import geda_hierpcb, pcb_to_thou


def add_subparsers(subparsers):
    geda_hierpcb.add_subparser(subparsers)
    pcb_to_thou.add_subparser(subparsers)
