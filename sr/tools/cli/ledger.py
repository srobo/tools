from __future__ import print_function


def command(args):
    import os
    import sys

    from sr.tools import spending
    from sr.tools.config import Config
    from sr.tools.environment import get_config_filename

    # Invoke ledger on the SR spending repo
    # Check that we are indeed invoking it on spending.git
    config = Config()

    # Default to using the spending.git specified in the config
    root = config["spending"]
    if root is not None:
        root = os.path.expanduser(root)
    else:
        # Not specified in the config
        root = os.getcwd()

    try:
        # Check that it's actually spending.git
        root = spending.find_root(path=root)
    except spending.NotSpendingRepo:
        print("This isn't SR spending.git", file=sys.stderr)
        print("Solve this by either:", file=sys.stderr)
        print(" - Changing working directory to spending.git", file=sys.stderr)
        print(" - Set the 'spending' config option in {}"
              .format(get_config_filename()), file=sys.stderr)
        sys.exit(1)

    ledger_args = ['ledger'] + args.command
    if "--file" not in args:
        # Tell ledger where to look
        ledger_args = ['ledger', "--file", os.path.join(root, "spending.dat")] \
            + args.command

    os.execvp("ledger", ledger_args)


def add_subparser(subparser):
    parser = subparser.add_parser('ledger', help='Open ledger.')
    parser.add_argument('command', nargs='*',
                        help='Commands passed straight to ledger.')
    parser.set_defaults(func=command)
