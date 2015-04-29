"""
A set of utilities that provide cross-platform support for a few basic
features.
"""
import os
import platform
import shlex
import struct
import subprocess
import sys


def open_editor(filename, fallback_editor='vim'):
    """
    Open the user-defined text editor on a particular file name and block until
    it exists.

    Parameters
    ----------
    filename : str
        The file to edit.
    fallback_editor : str
        The editor binary to fallback on if a suitable one cannot be
        determined.
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

    Parameters
    ----------
    components : str
        Used to separate out different parts of cache. Generally these are
        combined with the platform path separator path.

    Returns
    -------
    str
        The path to the cache directory.
    """
    if sys.platform == 'win32':
        default_path = os.path.join(os.environ['APPDATA'], 'SR', 'cache')
    else:
        default_path = os.path.expanduser('~/.sr/cache')

    root_path = os.environ.get('SR_CACHE_DIR', default_path)

    path = os.path.join(root_path, *components)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_config_filename():
    """
    Get the filename for the configuration file.

    Returns
    -------
    str
        The filename to the config.
    """
    default_path = os.path.expanduser('~/.sr/config.yaml')
    if sys.platform == 'win32':
        default_path = os.path.join(os.environ['APPDATA'], 'SR', 'config.yaml')

    return os.environ.get('SR_CONFIG', default_path)


def get_terminal_size():
    """
    Get the size of the terminal window the user is working in.

    The code for this is based on: https://gist.github.com/jtriley/1108174 .

    Returns
    -------
    (width, height) tuple
        A tuple containing the width and height as its elements respectively.
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
