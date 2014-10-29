from __future__ import print_function

import os
import sys


TOOLS = os.path.join( os.getenv("HOME"), ".sr", "tools" )

def get_commands( TOOLS ):
    """Returns a dict of all the available tools """
    cmds = {}

    # Find the executable files in the subdirectories
    for d in os.listdir( TOOLS ):
        if d in [".git"]:
            continue

        path = os.path.join( TOOLS, d )

        if os.path.isdir( path ):
            # Go through the files in this subdir
            for f in os.listdir(path):
                if f == "sr":
                    continue

                fp = os.path.join( path, f )

                if os.path.isfile(fp) and os.access( fp, os.X_OK ):
                    cmds[f] = fp

    return cmds


cmds = get_commands(TOOLS)

def main():
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] not in cmds.keys()):
        if len(sys.argv) > 1:
            print("Invalid command '%s'" % sys.argv[1])
        else:
            print("sr: The Student Robotics devtool wrapper script")
        print("Usage: sr COMMAND")
        print("Available commands:")

        k = sorted(cmds.keys())
        for cmd in k:
            if cmd[0] != "_" and cmd[-1] != "~":
                print("\t%s" % cmd)
        sys.exit(1)
    else:
        cmd = sys.argv[1]

    args = [cmd]
    args += sys.argv[2:]
    os.execv( cmds[cmd], args )
