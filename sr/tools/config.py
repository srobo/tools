"""Configuration for the tools."""
from __future__ import print_function

import getpass
import six
import sys

import yaml

try:
    import keyring
except ImportError:
    keyring = None

from sr.tools.environment import get_config_filename


if six.PY2:
    input = raw_input


class Config(dict):
    """Configuration reader for the tools."""
    def __init__(self):
        """
        Create a new configuration reader with the default configuration values
        set.
        """
        # default settings
        self['user'] = None
        self['use_keyring'] = False
        self['keyring_service'] = "SR tools"
        self['server'] = 'www.studentrobotics.org'
        self['https_port'] = 443
        self['spending'] = None

        # override with the local config
        try:
            self.update_from_file(get_config_filename())
        except IOError:
            pass

    def update_from_file(self, fname):
        """
        Update the config from the given YAML file

        :param str fname: The filename of the YAML file.
        :raises IOError: If the YAML file cannot be read.
        """
        with open(fname) as file:
            d = yaml.safe_load(file)

        if d is not None:
            self.update(d)

    def get_user(self, *args):
        """
        Get the username.

        Return the first non-None argument.
        If all arguments are None, get the username from the config.
        If the config doesn't provide the username, prompt the user
        for it.
        """
        for arg in args:
            if arg is not None:
                return arg

        user = self["user"]
        if user is not None:
            return user

        user = input("SR username: ")
        return user

    def get_password(self, *args, **kw):
        """
        Get the user's password.

        Return the first non-None argument.
        If all of the arguments are None, and the user has enabled the
        use of the keyring, attempts to look-up password in the
        keyring.  If that fails, resort to prompting the user for
        their password.

        For keyring lookups, a username is required.
        If the caller does not want to use the username specified
        by the config files for this, then the desired username can be
        fed in through the 'user' keyword argument.  This argument is
        ignored if its value is None.
        """
        for arg in args:
            if arg is not None:
                return arg

        if self["use_keyring"]:
            "Try getting the password from the keyring"

            if "user" in kw and kw["user"] is not None:
                user = kw["user"]
            else:
                user = self["user"]

            if keyring is None:
                print("Warning: Cannot import keyring module.",
                      file=sys.stderr)
            else:
                password = keyring.get_password(self["keyring_service"], user)
                if password is not None:
                    return password

        # We failed to get the password from the keyring, so prompt the
        # user for it
        password = getpass.getpass("SR password: ")

        if self["use_keyring"] and keyring is not None:
            # Store password in the keyring
            keyring.set_password(self["keyring_service"], user, password)

        return password
