from sr.tools.cli.trac import attach, depends_on, depgraph, deps_add, deps_rm


def add_subparsers(subparsers):
    attach.add_subparser(subparsers)
    depends_on.add_subparser(subparsers)
    depgraph.add_subparser(subparsers)
    deps_add.add_subparser(subparsers)
    deps_rm.add_subparser(subparsers)
