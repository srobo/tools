import os
import shlex
import subprocess


def open_editor(filename):
    editor = os.environ.get("EDITOR", "vim")
    args = shlex.split(editor)
    args.append(filename)
    subprocess.check_call(args)
