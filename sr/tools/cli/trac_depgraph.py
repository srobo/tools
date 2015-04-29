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

    tickets = {}

    done = set()
    todo = set([args.ticket])

    print("digraph G {")
    print("rankdir=LR;")

    while len(todo):
        for num in list(todo):
            t = Ticket(num, server)
            tickets[num] = t

            for dep in t.deps:
                if dep not in done:
                    todo.add(dep)

                print("{0} -> {1};".format(dep, num))

            done.add(num)
            todo.remove(num)

    for num, ticket in tickets.items():
        if args.summaries:
            label = "#{}: {}".format(num, ticket.summary)
        else:
            label = "#{}".format(num)
        props = {"label": label,
                 "URL": ticket.url}

        if ticket.status == "closed":
            props["style"] = "filled"
            props["color"] = "grey"

        propstr = ""
        for name, val in props.items():
            propstr += """{0}="{1}" """.format(name, val)

        print("{0} [{1}]".format(num, propstr))

    print("}")


def add_subparser(subparsers):
    parser = subparsers.add_parser('trac-depgraph',
                                   help="Produce a graph of a ticket's "
                                        "dependencies.")
    parser.add_argument("ticket", type=int, help="Ticket number to attach")
    parser.add_argument("-s", "--summaries", action='store_true',
                        help='include ticket summaries in the graph')
    parser.set_defaults(func=command)
