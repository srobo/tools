#-*- coding: utf-8 -*-#
from __future__ import print_function

from decimal import Decimal as D
import os
import six
import sys


if six.PY2:
    input = raw_input


class PurchaseItem(object):
    def __init__(self, info):
        self.desc = info["desc"]
        self.cost = D("%.2f" % info["cost"])


class Purchase(object):
    def __init__(self, pinfo):
        self.budget_line = pinfo["budget-line"]
        self.summary = pinfo["summary"]

        self.items = []
        for item in pinfo["items"]:
            if item["desc"] is None:
                continue

            i = PurchaseItem(item)
            self.items.append(i)


class SpendRequest(object):
    "Query the user for purchase information"
    def __init__(self, fname, delete_file=False):
        self.fname = fname
        self.delete_file = delete_file
        self._parse()

    @classmethod
    def from_editor(cls):
        "Present the user with a template in an editor"
        import pkg_resources
        import tempfile

        import yaml

        import sr.tools.environment

        # Temporary file for user to fill in
        fd, fname = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)

        # Fill in the temporary file from the template
        template = pkg_resources.resource_stream('sr.tools.cli',
                                                 'spend-template.yaml')

        with open(fname, 'wb') as file:
            file.write(template.read())

        while True:
            sr.tools.environment.open_editor(fname)

            try:
                spendreq = cls(fname, delete_file=True)
            except KeyError as e:
                print("Missing field:", e, file=sys.stderr)
                input("Press return to try again")
                continue
            except yaml.parser.ParserError as e:
                print("Error parsing your YAML", file=sys.stderr)
                print(e, file=sys.stderr)
                input("Press return to try again")
                continue
            else:
                break

        return spendreq

    def __del__(self):
        "Remove our temporary file"
        if self.delete_file:
            os.remove(self.fname)

    def _parse(self):
        "Parse our YAML file"
        import yaml

        with open(self.fname, "r") as f:
            data = yaml.load(f)

        self.username = data["username"]
        self.summary = data["summary"]
        self.supplier = data["supplier"]
        self.supplier_url = data.get("supplier-url", None)

        self.purchases = []
        for purchase in data["purchases"]:
            if purchase["budget-line"] is None:
                continue

            p = Purchase(purchase)
            self.purchases.append(p)


def command(args):
    import datetime

    import sr.tools.spending as srspending
    import sr.tools.budget as srbudget
    from sr.tools.trac import TracProxy, WrongServer

    try:
        spending_root = srspending.find_root()
    except srspending.NotSpendingRepo:
        print("Please run in spending.git top level directory",
              file=sys.stderr)
        sys.exit(1)

    try:
        budget = srspending.load_budget_with_spending(spending_root)
    except srbudget.NoBudgetConfig as nbc:
        print("Error:", nbc.message, file=sys.stderr)
        print("Have you initialised the budget submodule?", file=sys.stderr)
        print("If not, run 'git submodule update --init'.", file=sys.stderr)
        sys.exit(1)

    if args.spend_file is not None:
        spend_request = SpendRequest(args.spend_file)
    else:
        spend_request = SpendRequest.from_editor()

    ticket_text = "Payee: {} \\\\\n".format(spend_request.username)

    if spend_request.supplier_url is None:
        ticket_text += "Supplier: {} \\\\\n".format(spend_request.supplier)
    else:
        ticket_text += "Supplier: [{url} {supplier}] \\\\\n" \
                       .format(url=spend_request.supplier_url,
                               supplier=spend_request.supplier)

    budget_line_totals = {}

    for purchase in spend_request.purchases:
        try:
            budget_line = budget.path(purchase.budget_line)
        except KeyError:
            # TODO: Move this check up into the parser so it's caught and the
            # user can fix it
            print('Budget line "{0}" not found', file=sys.stderr)
            sys.exit(1)

        bl_request_total = D(0)

        ticket_text += """
    === Items from [budget:{budget_line}] ===
    {summary} \\\\
    ||= '''Item''' =||= '''Cost''' =||
    """.format(budget_line=purchase.budget_line,
               summary=purchase.summary)

        for item in purchase.items:
            ticket_text += "|| {desc} || £{cost} ||\n".format(desc=item.desc,
                                                              cost=item.cost)

            bl_request_total += item.cost

        # How much has already been spent against this budget line
        spent = budget_line.spent

        req_total = spent + bl_request_total

        # It is over the limit?
        if req_total > budget_line.cost:
            print("Warning: This purchase exceeds the budget line '{0}'"
                  .format(purchase.budget_line))
            print("\tBudget line's value: £{0}".format(budget_line.cost))
            print("\tRequested Expenditure: £{0} ({1}%)"
                  .format(req_total, 100 * (req_total) / budget_line.cost))
            if not input("Continue anyway? [y/N] ").lower() == 'y':
                sys.exit()

        if purchase.budget_line not in budget_line_totals:
            budget_line_totals[purchase.budget_line] = D(0)
        budget_line_totals[purchase.budget_line] += bl_request_total

    ticket_text += """
    === Budget Line Totals ===
    ||= '''Budget Line''' =||= '''Total''' =||
    """
    for line, total in budget_line_totals.items():
        ticket_text += "|| [budget:{line}] || £{total} ||\n" \
                       .format(line=line, total=total)

    print(ticket_text)

    if args.dry_run:
        print("Stopping before actually creating ticket.")
        sys.exit(0)

    try:
        server = TracProxy(server=args.server, port=args.port)
    except WrongServer:
        print("Error: The specified server is not a Trac instance",
              file=sys.stderr)
        sys.exit(1)

    ticketNum = server.ticket.create(spend_request.summary,
                                     ticket_text,
                                     {'component': "Purchasing",
                                      'owner': "treasurer",
                                      'type': "task"})

    if not ticketNum > 0:
        print("Unable to create a valid ticket")
        sys.exit()

    if args.port == 443:
        hostname = args.server
    else:
        hostname = "{0}:{1}".format(args.server, args.port)

    print("Purchasing ticket created: https://{0}/trac/ticket/{1}".format(
        hostname, ticketNum))

    print("Spending Entries:")

    for purchase in spend_request.purchases:
        print()
        today = datetime.date.today()

        i = "{date} ! {summary}\n"
        i += "    {account}\t£{amount}\n"
        i += "    Liabilities:{payee}\n"
        i += "    ; trac: #{trac}"

        print(i.format(date=today.isoformat(),
                       summary=purchase.summary,
                       account=srspending.budget_line_to_account(
                           purchase.budget_line),
                       amount=sum([x.cost for x in purchase.items]),
                       payee=spend_request.username,
                       trac=ticketNum))


def command_deprecated(args):
    print("This is deprecated, please use 'make-purchase' instead.",
          file=sys.stderr)
    command(args)


def add_subparser(subparsers):
    parser = subparsers.add_parser('make_purchase',
                                   help="Make an SR purchase request")
    parser.add_argument("-s", "--server", help="Hostname of server to talk to")
    parser.add_argument("-p", "--port", help="Server port number to talk to",
                        type=int)
    parser.add_argument("-f", "--spend-file",
                        help="Take spending info from this YAML file rather "
                             "than running an editor")
    parser.add_argument("--dry-run", action="store_true",
                        help="Process and check everything, but don't "
                             "actually create purchasing ticket")
    parser.set_defaults(func=command_deprecated)

    parser = subparsers.add_parser('make-purchase',
                                   help="Make an SR purchase request")
    parser.add_argument("-s", "--server", help="Hostname of server to talk to")
    parser.add_argument("-p", "--port", help="Server port number to talk to",
                        type=int)
    parser.add_argument("-f", "--spend-file",
                        help="Take spending info from this YAML file rather "
                             "than running an editor")
    parser.add_argument("--dry-run", action="store_true",
                        help="Process and check everything, but don't "
                             "actually create purchasing ticket")
    parser.set_defaults(func=command)
