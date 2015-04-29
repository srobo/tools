import pipes
import re
import subprocess
import os


DEFAULT_SERVER = 'studentrobotics.org'
DEFAULT_REPOROOT = '/var/www/html/ide/repos'


def _decode_if_not_none(x):
    if x is None:
        return None
    else:
        return x.decode('UTF-8')


def remote_cmd(cmd, server=DEFAULT_SERVER):
    """
    Run a remote SSH command on a server.

    :param str cmd: The command to run on the server.
    :param str server: The server to run the command on.
    :returns: The stdout and stderr responses, or None for each.
    :rtype: (str or None, str or None)
    """
    if ':' in server:
        parts = server.split(':')
        hostname = parts[0]
        port = int(parts[1])
    else:
        hostname = server
        port = 22

    cmdline = "ssh {hostname} -p {port} {cmd}".format(hostname=hostname,
                                                      port=port,
                                                      cmd=pipes.quote(cmd))
    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, shell=True)
    so, se = p.communicate()
    assert p.wait() == 0
    return (_decode_if_not_none(x) for x in (so, se))


def list_teams(reporoot=DEFAULT_REPOROOT, server=DEFAULT_SERVER):
    """
    Get a list of teams from the IDE.

    :param str reporoot: The root directory for repositories.
    :param str server: The server with the IDE.
    :returns: A list of teams.
    :rtype: list of str
    """
    so, se = remote_cmd("ls {0}".format(reporoot), server)

    r = re.compile("^[A-Z0-9]+$")
    teams = [x for x in so.splitlines() if r.match(x) is not None]
    return [x.strip() for x in teams]


class Repo(object):
    """
    Representing a repository on the IDE.

    :param str path: The path to the repository.
    :param str server: The server that the repository is on.
    """
    def __init__(self, path, server=DEFAULT_SERVER):
        """Create a new repository object."""
        self.path = path
        self.server = server

    def get_modtime(self):
        """
        Get the time of the last commit.

        :returns: The time as a single number.
        :rtype: int
        """
        cmd = 'cd {path}; git log -1 --format="format:%ct"'.format(
            path=pipes.quote(self.path)
        )

        so, se = remote_cmd(cmd, self.server)
        return int(so)

    def __repr__(self):
        return os.path.basename(self.path)


class Team(object):
    """
    Representing a team in the IDE.

    :param str identifier: The identifier of the team.
    :param str server: The server that the team resides in.
    :param str reporoot: The root of the repositories on that server.
    """
    def __init__(self, identifier, server=DEFAULT_SERVER,
                 reporoot=DEFAULT_REPOROOT):
        """Create a new team object."""
        self.identifier = identifier
        self.server = server
        self.reporoot = reporoot

        self._load_repos()

    def _load_repos(self):
        cmd = "ls {reporoot}/{team}/master/".format(reporoot=self.reporoot,
                                                    team=self.identifier)
        so, se = remote_cmd(cmd, self.server)
        repos = so.splitlines()

        self.repos = []
        for r in repos:
            path = '{root}/{team}/master/{repo}'.format(root=self.reporoot,
                                                        team=self.identifier,
                                                        repo=r)
            self.repos.append(Repo(path, self.server))
