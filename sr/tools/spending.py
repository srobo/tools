"Library for accessing the spending files"
from __future__ import print_function

import datetime
from decimal import Decimal as D
import errno
import os
from subprocess import check_output, check_call, CalledProcessError
import sys

import sr.tools.budget as budget


class Transaction(object):

    def __init__(self, name, date, fname):

        self.name = "TODO"
        self.date = None        # TODO
        self.summary = "TODO"
        self.description = "TODO"
        self.budget = "TODO"
        self.cost = D(0)        # TODO
        self.trac = 0           # TODO

        self.cheque = None      # TODO
        self.payee = None       # TODO
        self.ackdate = None     # TODO

        self.bank_transfer = False  # TODO

        # Strip the '.yaml' off the end of the budget field if it's present
        if self.budget[-5:] == ".yaml":
            self.budget = self.budget[:-5]


def load_transactions(root):
    root = os.path.abspath(root)
    transactions = []

    for dirpath, dirnames, filenames in os.walk(root):
        try:
            dirnames.remove(".git")
            dirnames.remove("budget")
        except ValueError:
            "Those directories will not always be there"
            pass

        for fname in filenames:
            fullp = os.path.abspath(os.path.join(dirpath, fname))

            if fname[-5:] != ".yaml":
                continue

            # The name of a transaction is not unique as multiple transactions
            # with the same file name can exist in the spending repository.
            name = fname[:-5]

            # The date of the transaction if it has been reconciled. None if
            # it's still pending.
            topdir = fullp[len(root) + 1:fullp.find('/', len(root) + 1)]
            repopath = fullp[len(root) + 1:-(len(fname) + 1)]
            if topdir == "pending":
                date = None
            else:
                try:
                    tmp = repopath.split("/")
                    date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                except:
                    print("Unable to determine the date of the transaction "
                          "%s." % fullp, file=sys.stderr)
                    exit(1)

            transactions.append(Transaction(name, date, fullp))
    return transactions


def group_trans_by_budget_line(trans):
    transgrp = {}
    for t in trans:
        if t.budget in transgrp:
            transgrp[t.budget].append(t)
        else:
            transgrp[t.budget] = [t]
    return transgrp


def budget_line_to_account(line):
    "Convert a budget line to an account name"
    if line[0] == "/":
        line = line[1:]
    line = line.replace("/", ":")
    return "Expenses:{0}".format(line)


def account_to_budget_line(account):
    "Convert an account name to a budget line name"
    line = account.replace(":", "/")
    return line[len("Expenses/"):]


class LedgerNotFound(Exception):

    def __init__(self):
        super(LedgerNotFound, self).__init__("Unable to find 'ledger' which "
                                             "is required to operate the "
                                             "spending repo.")


def load_budget_spends(root):
    p = os.path.join(root, "spending.dat")

    try:
        balances = check_output(["ledger",
                                 "--file", p,
                                 "bal",
                                 "--format", "%A,%(display_total)\n",
                                 "^Expenses:"])
    except OSError as oe:
        if oe.errno == errno.ENOENT:
            "A nicer error for the most likely case"
            raise LedgerNotFound
        else:
            "Re-raise the underlying exception"
            raise

    lines = {}

    for line in balances.splitlines():
        account, total = line.split(",")
        if len(account) == 0:
            continue

        total = D(total.decode("utf-8")[1:])
        line = account_to_budget_line(account)

        lines[line] = total

    return lines


def load_budget_with_spending(root):
    bud = budget.load_budget(os.path.join(root, "budget/"))
    lines = load_budget_spends(root)

    for b in bud.walk():
        if b.name not in lines:
            b.spent = D(0)
        else:
            b.spent = lines[b.name]

    return bud


class NotSpendingRepo(Exception):
    pass


def find_root(path=None):
    """
    Find the root directory of the spending repository.

    Checks that the repository is spending.git too.

    :param path: if provided, is a path within the spending.git repository
                 (defaults to working directory)
    """
    if path is None:
        path = os.getcwd()

    try:
        "Check that we're in spending.git"

        with open("/dev/null", "w") as n:
            check_call(["git", "rev-list",
                        # This is the commit that transitioned spending.git
                        # over to ledger, which is required for this library
                        "09d64df13422ac2fcf9bd17c00b1f66e9e78e912"],
                       cwd=path,
                       stdout=n,
                       stderr=n)
    except CalledProcessError:
        "It's not the spending repository"
        raise NotSpendingRepo

    root = check_output(["git", "rev-parse", "--show-toplevel"],
                        cwd=path)

    return root.strip().decode('utf-8')
