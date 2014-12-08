import pipes
import re
import subprocess
import os


DEFAULT_SERVER = 'studentrobotics.org'
DEFAULT_REPOROOT = '/var/www/html/ide/repos'


def decode_if_not_none(x):
    if x is None:
        return None
    else:
        return x.decode('UTF-8')


def remote_cmd(cmd, server=DEFAULT_SERVER):
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
    return (decode_if_not_none(x) for x in (so, se))


def list_teams(reporoot=DEFAULT_REPOROOT, server=DEFAULT_SERVER):
    "Return a list of team numbers"
    so, se = remote_cmd("ls {0}".format(reporoot), server)

    r = re.compile("^[A-Z0-9]+$")
    teams = [x for x in so.splitlines() if r.match(x) is not None]
    return [x.strip() for x in teams]


class Repo(object):

    def __init__(self, path, server=DEFAULT_SERVER):
        self.path = path
        self.server = server

    def get_modtime(self):
        """Get the time of the last commit."""
        cmd = 'cd {path}; git log -1 --format="format:%ct"'.format(
            path=pipes.quote(self.path)
        )

        so, se = remote_cmd(cmd, self.server)
        return int(so)

    def __repr__(self):
        return os.path.basename(self.path)


class Team(object):

    def __init__(self, identifier, server=DEFAULT_SERVER,
                 reporoot=DEFAULT_REPOROOT):
        self.identifier = identifier
        self.server = server
        self.reporoot = reporoot
        self._pop_repos()

    def _pop_repos(self):
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
