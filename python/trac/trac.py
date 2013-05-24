from xmlrpclib import ServerProxy

class WrongServer(Exception):
    "The RPC server specified isn't a trac instance"
    pass

class TracProxy(ServerProxy):
    def __init__( self,
                  user, password 
                  server = "www.studentrobotics.org",
                  port = 443 ):
        rpc_url = "https://{user}:{password}@{server}:{port}/trac/login/rpc".format(
                user = user,
                password = password,
                server = server,
                port = port )

        ServerProxy.__init__(self, rpc_url)

        if "ticket.create" not in self.system.listMethods():
            raise WrongServer
