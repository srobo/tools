from sr import Config
import sys
from xmlrpclib import ServerProxy

class WrongServer(Exception):
    "The RPC server specified isn't a trac instance"
    pass

class TracProxy(ServerProxy):
    def __init__( self,
                  user = None,
                  password = None,
                  server = None,
                  port = None,
                  anon = False ):

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
