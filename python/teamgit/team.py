import subprocess, re

SERVER = "srobo.org"
REPOROOT = "/var/www/html/ide/repos"

def remote_cmd(cmd):
    p = subprocess.Popen( "ssh {server} {cmd}".format( server = SERVER,
                                                       cmd = cmd ),
                          stdout = subprocess.PIPE,
                          shell = True )

    so, se = p.communicate()
    assert p.wait() == 0
    return so, se

def list_teams():
    "Return a list of team numbers"
    so, se = remote_cmd( "ls {0}".format( REPOROOT ) )

    r = re.compile( "^[0-9]+$" )

    teams = [ x for x in so.splitlines() if r.match(x) != None ]

    return [int(x) for x in teams]

class Team(object):
    def __init__(self, teamno):
        self.teamno = int(teamno)

    def list_repos(self):
        so, se = remote_cmd( "ls {reporoot}/{teamno}/master/".format(
                reporoot = REPOROOT,
                teamno = self.teamno ) )
        repos = so.splitlines()

        return repos

