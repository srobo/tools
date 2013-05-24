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
                  port = None ):

        config = Config()
        user = config.get_user( user )
        password = config.get_password( password, user = user )

        if server is None:
            server = config["server"]

        if port is None:
            port = config["https_port"]

        rpc_url = "https://{user}:{password}@{server}:{port}/trac/login/rpc".format(
                user = user,
                password = password,
                server = server,
                port = port )

        ServerProxy.__init__(self, rpc_url)

        if "ticket.create" not in self.system.listMethods():
            raise WrongServer
