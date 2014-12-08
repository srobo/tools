from __future__ import print_function


def command(args):
    import os
    import sys
    from six.moves.xmlrpc_client import Binary

    from sr.tools.trac import TracProxy, WrongServer

    try:
        server = TracProxy(server=args.server, port=args.port)
    except WrongServer:
        print("Error: The specified server is not a Trac instance",
              file=sys.stderr)
        sys.exit(1)

    with open(args.filename, "r") as f:
        content = f.read()

    server.ticket.putAttachment(args.ticket, os.path.basename(args.filename),
                                args.desc, Binary(content))


def add_subparser(subparsers):
    parser = subparsers.add_parser('trac-attach',
                                   help="Attach a file to a trac ticket")
    parser.add_argument("-s", "--server",
                        help="Hostname of server to talk to")
    parser.add_argument("-p", "--port", type=int,
                        help="Server port number to talk to")
    parser.add_argument("-d", "--desc", default="",
                        help="File description")
    parser.add_argument("ticket", type=int,
                        help="Ticket number to attach to")
    parser.add_argument("filename", help="File to attach")
    parser.set_defaults(func=command)
