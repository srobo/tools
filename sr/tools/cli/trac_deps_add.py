#!/usr/bin/env python
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

    t = Ticket(args.ticket, server)

    current = set(t.deps)
    new = set(args.deps)

    to_add = new - current
    already = new - to_add

    if len(already):
        for n in already:
            print('#{0} is already a dep of #{1}'.format(n, args.ticket),
                  file=sys.stderr)

    if len(to_add) == 0:
        sys.exit("No new dependencies to add to #{0}".format(args.ticket))

    t.deps += to_add

    if args.m is not None:
        msg = args.m
        msg += "\n\n"
    else:
        msg = ""

    msg += "Adding dependencies:"
    for n in to_add:
        msg += "\n * #{0}".format(n)

    updated = t.cleanup(dry_run=args.dry_run, msg=msg)

    if updated:
        if args.dry_run:
            print("Ticket would have been updated if not for --dry-run.")
        else:
            print("Ticket updated.")


def add_subparser(subparsers):
    parser = subparsers.add_parser('trac-deps-add',
                                   help="Add dependencies to a ticket")
    parser.add_argument("ticket", type=int, help="Ticket number")
    parser.add_argument("deps", type=int, nargs="+", help="Tickets to add")
    parser.add_argument("-m", type=str, help="Message to append")
    parser.add_argument("--dry-run", action="store_true",
                        help="Go through the motions, but don't commit the "
                             "change.")
    parser.set_defaults(func=command)
