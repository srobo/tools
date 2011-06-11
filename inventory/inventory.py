import os, subprocess, yaml
import assetcode
import sys

def gettoplevel():
    """Find the top level of the inventory repo"""
    tmp = subprocess.Popen(("git", "rev-parse", "--show-toplevel"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    gitdir = tmp.communicate()[0].strip()

    if tmp.returncode != 0:
        return None

    usersfn = os.path.join(gitdir, ".meta", "users")

    if not os.path.isfile(usersfn):
        return None
    return gitdir

def getusername():
    gitname = subprocess.Popen(("git", "config", "user.name"), stdout=subprocess.PIPE).communicate()[0].strip()
    gitemail = subprocess.Popen(("git", "config", "user.email"), stdout=subprocess.PIPE).communicate()[0].strip()

    return "%s <%s>" % (gitname, gitemail)

def getusernumber(gitdir, user):
    """Get the ID number of user"""
    usersfn = os.path.join(gitdir, ".meta", "users")
    f = open(usersfn)
    users = yaml.load(f)
    f.close()

    if users == None or user not in users:
        print "Inventory user \"%s\" not found.\nPlease see http://srobo.org/trac/wiki/Inventory for more information" % user
        sys.exit(3)

    return users[user]

def getpartnumbers(topd):
    """Recursively get a list of all part numbers"""
    parts = []

    for d in os.listdir(topd):
        if d in [".git", ".meta"]:
            continue

        path = os.path.join(topd, d)

        if os.path.isdir(path):
            parts.extend(getpartnumbers(path))
            try:
                acode = d[d.rindex("-sr")+3:]
            except:
                continue
            parts.append(assetcode.code_to_num(acode))
        elif os.path.isfile(path):

            if path[-1] == "~":
                "Ignore temporary files from editors"
                continue

            fname = os.path.basename(path)
            try:
                acode = fname[fname.rindex("-sr")+3:]
            except:
                continue
            parts.append(assetcode.code_to_num(acode))

    return parts

def getpartnumber(gitdir, userno):
    """Get the next available part number"""
    maxno = -1
    # Gather all part numbers from the inventory
    partnos = getpartnumbers(gitdir)
    for p in partnos:
        if p[0] == userno:
            maxno = max(maxno, p[1])
    return maxno+1
