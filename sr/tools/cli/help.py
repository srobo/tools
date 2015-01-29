import webbrowser

URL_PATTERN = 'http://srtools.readthedocs.org/en/latest/commands/{cmd}.html'


def command(args):
    for cmd in args.command:
        url = URL_PATTERN.format(cmd=cmd)
        webbrowser.open_new_tab(url)

def add_subparser(subparsers):
    parser = subparsers.add_parser('help',
                                   help='Get information about an sr command.')
    parser.add_argument('command', nargs='+', help='Commands to get help about')
    parser.set_defaults(func=command)
