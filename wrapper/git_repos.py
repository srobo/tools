# Git directories:
import sys, os, subprocess

gits = { 
    "gedashield": { "url": "git://gitorious.org/gedashield/mainline.git",
                    "commit": "fca3559c7998cdff4d53980529b478d585a87264",
                    "commands" : [ "ods2trag/ods2trag.py", 
                                   "pcbfoot/dil_ic.py",
                                   "pcbfoot/smd-ic.py" ] }
    }

class GitRepo:
    def __init__(self, name, desc, TOOLS_DIR):
        self.repo = os.path.join( TOOLS_DIR, "git", name )
        self.desc = desc
        self.name = name
        self.state = [ "    - %s: " % name ]
        self.state_last_len = 0

        if not os.path.exists( self.repo ):
            self.clone()

    def __state_push( self, msg ):
        self.state.append(msg)
        self.__state_update()

    def __state_pop( self ):
        self.state.pop()
        self.__state_update()

    def __state_update( self ):
        sys.stdout.write("\r")
        sys.stdout.write(" " * self.state_last_len)
        sys.stdout.flush()
        sys.stdout.write("\r")
        self.state_last_len = 0

        for x in self.state:
            self.state_last_len += len(x)
            sys.stdout.write( x )
        sys.stdout.flush()

    def clone(self):
        # Clone the repo:
        self.__state_push("cloning")
        p = subprocess.Popen( "git clone -q %s %s" % ( self.desc["url"], self.name ),
                              cwd = os.path.normpath( os.path.join( self.repo, "../" ) ),
                              shell = True )
        p.communicate()
        if p.wait() != 0:
            print "FAIL: Couldn't clone.  Aborting."
            sys.exit(1)
        self.__state_pop()

    def update(self):
        """Updates the given repo to the given commit"""
        self.__state_push("fetching")

        # Fetch the latest changes
        p = subprocess.Popen( "git fetch -q origin",
                              cwd = self.repo,
                              shell = True )
        p.communicate()
        if p.wait() != 0:
            print "FAIL: Couldn't fetch.  Aborting."
            sys.exit(1)

        self.__state_pop()

        self.__state_push("checking out")
        # Checkout the commit we want
        p = subprocess.Popen( "git checkout -q %s" % self.desc["commit"],
                              cwd = self.repo,
                              shell = True )
        p.communicate()
        if p.wait() != 0:
            print "FAIL: Couldn't checkout.  Aborting."
            sys.exit(1)
        self.__state_pop()

    def __get_hash(self):
        """Returns the currently checked out commit hash for the given repo"""
        f = open( os.path.join( self.repo, ".git/HEAD" ) )
        h = f.read()
        f.close()

        return h.strip()

    def check(self):
        if self.__get_hash() != self.desc["commit"]:
            self.update()

def update_all( TOOLS_DIR ):
    for name, git in gits.iteritems():
        print "\t- %s..." % name,
        sys.stdout.flush()

        repo = GitRepo( name, git, TOOLS_DIR )
        repo.update()

        print "done."

def check_all( TOOLS_DIR ):
    for name, git in gits.iteritems():
        repo = GitRepo( name, git, TOOLS_DIR )
        repo.check()
