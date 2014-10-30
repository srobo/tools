from sr.tools import Config
import sys

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy


class WrongServer(Exception):
    "The RPC server specified isn't a trac instance"
    pass


class TracProxy(ServerProxy):
    "An XML-RPC proxy for SR Trac"

    def __init__( self,
                  user = None,
                  password = None,
                  server = None,
                  port = None,
                  anon = False ):
        """Initialise an SR trac object

        Arguments:
        user -- The username.  By default this is looked up in the
                config or the user is prompted for it.
        password -- The password to use.  If left as its default value
                    of None, it may be looked up in the keyring, or
                    the user may be prompted for it.
        server -- The server hostname.  Defaults to that found in the
                  config.
        port -- The HTTPS port of the server.  Defaults to that found
                in the config.
        anon -- Whether to use trac anonymously.
        """

        config = Config()

        if server is None:
            server = config["server"]

        if port is None:
            port = config["https_port"]

        rpc_settings = { "server": server,
                         "port": port }

        if anon:
            rpc_url = "https://{server}:{port}/trac/rpc"
        else:
            rpc_url = "https://{user}:{password}@{server}:{port}/trac/login/rpc"

            user = config.get_user( user )
            rpc_settings["user"] = user
            rpc_settings["password"] = config.get_password( password,
                                                            user = user )

        rpc_url = rpc_url.format( **rpc_settings )

        ServerProxy.__init__(self, rpc_url)

        if "ticket.create" not in self.system.listMethods():
            raise WrongServer
