from __future__ import print_function


def command(args):
    import sys

    from sr.tools.trac import Ticket, TracProxy, WrongServer

    try:
        server = TracProxy()
    except WrongServer:
        print("Error: The specified server is not a Trac instance",
              file=sys.stderr)
        sys.exit(1)

    search_ticket = args.ticket

    query = "description=~{}".format(search_ticket)
    matches = server.ticket.query(query)

    deps = []
    refs = []
    for num in matches:
        t = Ticket(num, server)
        if search_ticket in t.deps:
            deps.append(t)
        else:
            refs.append(t)

    if len(deps):
        print("The following tickets depend on {}:".format(search_ticket))
        for t in deps:
            print("\t{} [{}]".format(t, t.url))
    else:
        print("Nothing depends on {}".format(search_ticket))

    if len(refs):
        print("The following tickets appear to reference {}:"
              .format(search_ticket))
        for t in refs:
            print("\t{} [{}]".format(t, t.url))


def add_subparser(subparsers):
    parser = subparsers.add_parser('trac-depends-on',
                                   help='Show the items which have the given '
                                        'ticket as an immediate dependency.')
    parser.add_argument("ticket", type=int, help="Ticket number")
    parser.set_defaults(func=command)
