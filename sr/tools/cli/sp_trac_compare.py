from __future__ import print_function


def command(args):
    import sys

    from sr.tools import spending
    from sr.tools.trac import TracProxy

    transactions = spending.load_transactions("./")
    p = TracProxy(anon=True)
    tickets = p.ticket.query(
        "component=purchasing&max=0&resolution=fixed&status=closed")

    counts = {}
    for t in tickets:
        if t < 821 and t not in []:
            # Tickets before #839 except for those listed above weren't
            # budgeted
            continue

        counts[t] = 0

    # Tickets that have been prematurely added to spending.git
    premature = []

    for t in transactions:
        if t.trac not in counts:
            premature.append(t.trac)
            continue

        counts[t.trac] += 1

    missing = []
    for tnum, count in counts.items():
        if count == 0:
            missing.append(tnum)

    missing.sort()

    if len(missing):
        print("{0} trac tickets with no spending.git "
              "entry:".format(len(missing)))
        for t in missing:
            print("{0:10} -- http://srobo.org/trac/ticket/{0}".format(t))
    else:
        print("All resolved purchasing tickets exist in spending.git :-)")

    if len(premature):
        print("-" * 40)
        print("Grabbing ticket information...", end='')
        sys.stdout.flush()

        states = {}
        for t in premature:
            info = p.ticket.get(t)[3]
            s = (info["status"], info["resolution"])

            if s not in states:
                states[s] = []

            states[s].append(t)

        print("done")

        print("{0} purchasing tickets have been added to spending.git "
              "before being closed.".format(len(premature)))
        print()
        print("This is non-fatal, "
              "and generally means that there is more treasurer-related")
        print("action to be taken on them "
              "(maybe the treasurer is waiting for some information).")
        print()

        for state, tickets in states.items():
            tickets.sort()

            print("{0} tickets in state {1}:{2}:".format(len(tickets),
                                                         state[0],
                                                         state[1]))
            for t in tickets:
                print("{0:10} -- http://srobo.org/trac/ticket/{0}".format(t))
            print()

    open_tickets = set(p.ticket.query("component=purchasing&max=0&status=new"))

    print("There are {0} unresolved purchasing tickets in trac right now."
          .format(len(open_tickets)))
    print("Here are the ones that don't exist in spending.git")
    print("(note that they don't need to yet)")

    n = list(open_tickets.difference(premature))
    n.sort()

    for t in n:
        print("{0:10} -- http://srobo.org/trac/ticket/{0}".format(t))


def add_subparser(subparsers):
    parser = subparsers.add_parser('sp-trac-compare',
                                   help='Compare spending with trac.')
    parser.set_defaults(func=command)
