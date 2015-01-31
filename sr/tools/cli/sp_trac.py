#-*- coding: utf-8 -*-#
from __future__ import print_function


def command(args):
    import re
    import sys
    import six.moves.xmlrpc_client as xmlrpclib

    from sr.tools import spending
    from sr.tools.trac import TracProxy

    try:
        root = spending.find_root()
    except spending.NotSpendingRepo:
        print(
            "Please run in spending.git top level directory", file=sys.stderr)
        exit(1)

    spends = spending.load_transactions(root)

    spendsumgrp = {}
    for s in spends:
        if s.trac in spendsumgrp:
            spendsumgrp[s.trac] += float(s.cost)
        else:
            spendsumgrp[s.trac] = float(s.cost)

    server = TracProxy(anon=True)
    mserver = xmlrpclib.MultiCall(server)

    tickets = server.ticket.query("status!=closed&component=Purchasing")
    for ticket in tickets:
        mserver.ticket.get(ticket)

    costsumgrp = {}
    for ticket in mserver():
        match = re.search(
            'Total cost: \xa3([0-9.]+)', ticket[3]['description'])
        if match is None:
            print("Unable to determine cost for ticket " +
                  str(ticket[0]) + ". Invalid formatting")
            continue

        if ticket[0] in costsumgrp:
            costsumgrp[ticket[0]] += float(match.groups()[0])
        else:
            costsumgrp[ticket[0]] = float(match.groups()[0])

    for val in costsumgrp:
        if spendsumgrp[val] != costsumgrp[val]:
            print("Ticket " + str(val) + " does not match transactions")
            print("\tTicket cost:  £" + str(costsumgrp[val]))
            print("\tTransactions: £" + str(spendsumgrp[val]))


def add_subparser(subparsers):
    parser = subparsers.add_parser('sp-trac', help='Check spending with trac.')
    parser.set_defaults(func=command)
