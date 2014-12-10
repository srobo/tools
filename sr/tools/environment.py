"""
A set of utilities that provide cross-platform support for a few basic
features.
"""
import os
import shlex
import subprocess
import sys


def open_editor(filename, fallback_editor='vim'):
    """
    Open the user-defined text editor on a particular file name and block until
    it exists.

    :param str filename: The file to edit.
    :param str fallback_editor: The editor binary to fallback on if a suitable
                                one cannot be determined.
    """
    editor = os.environ.get("EDITOR", fallback_editor)
    args = shlex.split(editor)
    args.append(filename)
    subprocess.check_call(args)


def get_cache_dir(*components):
    """
    Return the cache directory for a particular component of the tools.

    If the environment variable ``SR_CACHE_DIR`` is set, that takes precedence
    as the root of the cache directory.

    This function will endeavour to create the cache directory for you.

    :param str components: Components used to separate out different parts of
                           cache. Generally these are combined with the
                           platform path separator path.
    :returns: The path to the cache directory.
    :rtype: str
    """
    default_path = os.path.expanduser('~/.sr/cache')
    if sys.platform == 'win32':
        default_path = os.path.join(os.environ['APPDATA'], 'SR', 'cache')

    root_path = os.environ.get('SR_CACHE_DIR', default_path)

    path = os.path.join(root_path, *components)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_config_filename():
    """
    Get the filename for the configuration file.

    :returns: The filename to the config.
    :rtype: str
    """
    default_path = os.path.expanduser('~/.sr/config.yaml')
    if sys.platform == 'win32':
        default_path = os.path.join(os.environ['APPDATA'], 'SR', 'config.yaml')

    return os.environ.get('SR_CONFIG', default_path)
