from __future__ import print_function

import os
import sys
import subprocess

from sr.tools import __path__


def get_commands_directory():
    """Return the directory at which commands will be found."""
    return os.path.join(__path__[0], "cmds")


def find_commands(commands_dir=None):
    """
    Recursively find commands and return a dictionary mapping name to full file
    path.
    """
    if commands_dir is None:
        commands_dir = get_commands_directory()

    cmds = {}
    for d in os.listdir(commands_dir):
        if d in [".git"]:
            continue

        path = os.path.join(commands_dir, d)

        if os.path.isdir(path):
            # Go through the files in this subdir
            for f in os.listdir(path):
                if f == "sr":
                    continue

                fp = os.path.join(path, f)

                if os.path.isfile(fp) and os.access(fp, os.X_OK):
                    cmds[f] = fp

    return cmds


def main():
    cmds = find_commands()

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
    if os.name == 'nt':
        # this is hacky, and will be replaced with modules
        subprocess.call( ["python", cmds[cmd]] + args[2:] )
    else:
        os.execv( cmds[cmd], args )
