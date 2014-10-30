import os

from sr.tools.config import Config


def get_commands_directory():
    return os.path.join(__path__[0], "cmds")


def find_commands():
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
