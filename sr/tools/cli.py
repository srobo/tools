from __future__ import print_function

import os
import sys

from sr.tools import find_commands

cmds = find_commands()

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
