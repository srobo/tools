from collections import Counter
import re

from six.moves.xmlrpc_client import ServerProxy

from sr.tools.config import Config


class WrongServer(Exception):
    """The RPC server specified isn't a trac instance."""
    pass


class TracProxy(ServerProxy):
    """
    An XML-RPC proxy for SR Trac.

    :param user: The username. By default this is looked up in the config
                 or the user is prompted for it.
    :param password: The password to use. If left as its default value of
                     None, it may be looked up in the keyring, or the user
                     may be prompted for it.
    :param server: The server hostname. Defaults to that found in the
                   config.
    :param port: The HTTPS port of the server. Defaults to that found in
                 the config.
    :param anon: Whether to use trac anonymously.
    """
    def __init__(self, user=None, password=None, server=None, port=None,
                 anon=False):
        """Initialise an SR trac object."""
        config = Config()

        if server is None:
            server = config["server"]

        if port is None:
            port = config["https_port"]

        self.server = server
        self.port = port

        rpc_settings = {"server": server, "port": port}

        if anon:
            rpc_url = "https://{server}:{port}/trac/rpc"
        else:
            rpc_url = "https://{user}:{password}@{server}:{port}/trac/login" \
                      "/rpc"

            user = config.get_user(user)
            rpc_settings["user"] = user
            rpc_settings["password"] = config.get_password(password, user=user)

        rpc_url = rpc_url.format(**rpc_settings)

        ServerProxy.__init__(self, rpc_url)

        if 'ticket.create' not in self.system.listMethods():
            raise WrongServer()


class Ticket(object):
    """
    A ticket that may have dependencies.

    :param int num: The ticket number.
    :param proxy: The XMLRPC proxy object.
    """
    def __init__(self, num, proxy):
        """Create a new ticket object."""
        self.proxy = proxy
        self.num = num
        self.refresh()

    def refresh(self):
        """Refresh with data from trac."""
        _, _, _, ticket = self.proxy.ticket.get(self.num)
        desc = self.desc = ticket["description"]
        self.status = ticket["status"]
        self.resolution = ticket["resolution"]
        self.summary = ticket["summary"]
        self.changetime = ticket["changetime"]
        self.component = ticket["component"]
        self.keywords = ticket["keywords"]
        self.milestone = ticket["milestone"]
        self.owner = ticket["owner"]
        self.cc = ticket["cc"]
        self.priority = ticket["priority"]
        self.reporter = ticket["reporter"]
        self.time = ticket["time"]
        self.type = ticket["type"]
        self.version = ticket["version"]

        reg = self._construct_regex()

        self.deps = []

        r = reg.match(desc)
        if r is None:
            # ticket has no dependencies
            self.prelude = desc
            self.deptitle = ""
            self.depspace = ""
            self.deplist = ""
            self.postscript = ""
            self.deplist_ends_in_newline = False
            self.list_prefix = ""
            return

        self.prelude = r.group("prelude")
        self.deptitle = r.group("deptitle")
        self.depspace = r.group("depspace")
        self.deplist = r.group("deplist")
        self.postscript = r.group("postscript")

        spacings = Counter()

        regex = r"^(\s*\*\s*)#([0-9]+)\s*(.*)$"
        opts = re.MULTILINE | re.IGNORECASE
        for asterisk, ticket_num, desc in re.findall(regex, self.deplist,
                                                     opts):
            spacings.update([asterisk])
            self.deps.append(int(ticket_num))

        self.list_prefix = spacings.most_common(1)[0][0]
        self.deplist_ends_in_newline = (self.deplist[-1] == "\n")

    @property
    def url(self):
        server, port = self.proxy.server, self.proxy.port
        if port == 443:
            base = 'https://{server}/trac/ticket/{num}'
        else:
            base = 'https://{server}:{port}/trac/ticket/{num}'
        return base.format(server=server,
                           port=port,
                           num=self.num)

    def cleanup(self, dry_run=False,
                msg="Synchronise dependency summaries with dependencies "
                    "(automated edit)"):
        """
        Clean-up the ticket's description.

        :param bool dry_run: Whether or not to actually commit the changes.
        :param str msg: The message to be shown in Trac.
        :returns: Whether or not a change has occurred.
        :rtype: bool
        """

        # Rebuild the deplist:
        if len(self.deps) != 0 and self.deptitle == "":
            self.deptitle = "\n\nDependencies:\n"
            self.list_prefix = " * "

        d = self.prelude + self.deptitle + self.depspace

        for i, ticket_num in enumerate(self.deps):
            _, _, _, dep = self.proxy.ticket.get(ticket_num)

            d += "{prefix}#{num} {summary}".format(prefix=self.list_prefix,
                                                   num=ticket_num,
                                                   summary=dep["summary"])

            if i != len(self.deps) - 1 or self.deplist_ends_in_newline:
                d += "\n"

        d += self.postscript

        if d == self.desc:
            # description has not changed
            return False

        if not dry_run:
            self.proxy.ticket.update(self.num, msg, {"description": d})

        self.refresh()
        return True

    def _construct_regex(self):
        # Construct a regexp for splitting dependencies from the prelude
        # Prelude section:
        reg = r"(?P<prelude>.*)"

        # Dependencies line
        reg += r"(?P<deptitle>^Dependencies:?$)"

        # Possible newlines between dependencies line and dependency list
        reg += r"(?P<depspace>\s*\n)?"

        # Dependency list:
        reg += r"(?P<deplist>(^\s*\*[^\n]+($\n|\Z))*)"

        # Postscript after the dependency list:
        reg += r"(?P<postscript>.*)"

        return re.compile(reg, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    def __str__(self):
        return "{0}: {1}".format(self.num, self.summary)
