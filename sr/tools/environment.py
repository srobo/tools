import os
import shlex
import subprocess


def open_editor(filename):
    """
    Open the user-defined text editor on a particular file name and block until
    it exists.
    """
    editor = os.environ.get("EDITOR", "vim")
    args = shlex.split(editor)
    args.append(filename)
    subprocess.check_call(args)


def get_cache_dir(*components):
    """
    Return the cache directory for a particular component of the tools.

    If the environment variable 'SR_CACHE_DIR' is set, that takes precedence as
    the root of the cache directory.
    """
    root_path = os.path.expanduser(os.environ.get('SR_CACHE_DIR',
                                                  '~/.sr/cache'))

    path = os.path.join(root_path, *components)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
