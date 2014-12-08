from __future__ import print_function


BASE_URL = 'https://www.studentrobotics.org/.git/'


def fetch(url):
    import sys

    from six.moves.urllib.request import urlopen

    page = urlopen(url)
    data = page.read()

    if data is None:
        print('Failed to download from: {url}.'.format(url=url),
              file=sys.stderr)
        sys.exit(1)

    return data.strip().decode('utf-8')


def command(args):
    quiet = args.quiet

    url = BASE_URL + "HEAD"
    data = fetch(url)

    ref_base = 'ref: '

    # it's a hash
    if data[:len(ref_base)] != ref_base:
        print(data[:9])
        exit(0)

    ref = data[len(ref_base):]
    if not quiet:
        print('On:', ref)

    url = BASE_URL + ref
    data = fetch(url)
    print(data)


def add_subparser(subparsers):
    parser = subparsers.add_parser('srweb-version',
                                   help='Display the srweb version.')
    parser.add_argument('--quiet', '-q', action='store_true', dest='quiet',
                        help='Enable quiet mode.')
    parser.set_defaults(func=command)
