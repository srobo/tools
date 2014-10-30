import pipes
import re
import subprocess
import os


SERVER = 'srobo.org'
REPOROOT = '/var/www/html/ide/repos'


def remote_cmd(cmd):
    cmdline = "ssh {server} {cmd}".format(server=SERVER, cmd=pipes.quote(cmd))
    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, shell=True)
    so, se = p.communicate()
    assert p.wait() == 0
    return so, se


def list_teams():
    "Return a list of team numbers"
    so, se = remote_cmd("ls {0}".format(REPOROOT))

    r = re.compile("^[0-9]+$")
    teams = [x for x in so.splitlines() if r.match(x) != None]

    return [int(x) for x in teams]


class Repo(object):
    def __init__(self, path):
        self.path = path

    def get_modtime( self ):
        "Get the time of the last commit"

        cmd = 'cd {path}; git log -1 --format="format:%ct"'.format(
            path=pipes.quote(self.path)
        )
        so, se = remote_cmd(cmd)
        return int(so)

    def __repr__(self):
        return os.path.basename(self.path)


class Team(object):
    def __init__(self, teamno):
        self.teamno = int(teamno)
        self._pop_repos()

    def _pop_repos(self):
        cmd = "ls {reporoot}/{teamno}/master/".format(reporoot=REPOROOT,
                                                      teamno=self.teamno)
        so, se = remote_cmd(cmd)
        repos = so.splitlines()

        self.repos = []
        for r in repos:
            path = '{root}/{teamno}/master/{repo}'.format(root=REPOROOT,
                                                          teamno=self.teamno,
                                                          repo=r)
            self.repos.append(Repo(path))
