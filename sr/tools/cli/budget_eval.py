#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function


def command(args):
    from decimal import Decimal as D
    import sympy
    import sys

    import sr.tools.budget as budget

    try:
        root = budget.find_root()
    except budget.NotBudgetRepo:
        print("Error: Please run in budget.git", file=sys.stderr)
        exit(1)

    t = budget.load_budget(root)

    config = None

    # find the first BudgetItem to get its config
    for i in t.walk():
        if isinstance(i, budget.BudgetItem):
            config = i.conf
            break

    assert config is not None

    r = sympy.S(args.expression)
    r = D("%.2f" % r.evalf(subs=config.vars))

    print(r)


def add_subparser(subparsers):
    parser = subparsers.add_parser('budget-eval',
                                   help='Evaluate an expression on the '
                                        'budget.')
    parser.add_argument('expression', help='Expression to evaluate.')
    parser.set_defaults(func=command)
