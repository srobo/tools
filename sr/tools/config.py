"Config for the SR tools"
from __future__ import print_function

import getpass
import os
from subprocess import check_output
import sys
import yaml

try:
    import keyring
except ImportError:
    keyring = None

from sr.tools.environment import get_config_filename


class Config(dict):
    "Configuration reader for the SR tools"

    def __init__(self):
        # Load the config from ${THIS_REPO}/config.yaml
        self.update_from_file( os.path.join( self.get_tools_root(),
                                             "config.yaml" ) )

        # Override with the local config
        try:
            self.update_from_file(get_config_filename())
        except FileNotFoundError:
            pass

    @staticmethod
    def get_tools_root():
        "Return the root directory of tools.git"

        # Discover our directory
        mydir = os.path.dirname( __file__ )

        # Find the root of this git repo
        root = check_output( [ "git", "rev-parse", "--show-toplevel" ],
                             cwd = mydir )

        return root.decode("utf-8").strip()

    def update_from_file(self, fname):
        "Update the config from the given YAML file"

        with open(fname) as f:
            d = yaml.load(f, Loader = yaml.CLoader )

        self.update(d)

    def get_user(self, *args):
        """Get the username

        Return the first non-None argument.
        If all arguments are None, get the username from the config.
        If the config doesn't provide the username, prompt the user
        for it."""

        for arg in args:
            if arg is not None:
                return arg

        user = self["user"]
        if user is not None:
            return user

        user = raw_input( "SR username: " )
        return user

    def get_password(self, *args, **kw):
        """Get the user's password

        Return the first non-None argument.
        If all of the arguments are None, and the user has enabled the
        use of the keyring, attempts to look-up password in the
        keyring.  If that fails, resort to prompting the user for
        their password.

        For keyring lookups, a username is required.
        If the caller does not want to use the username specified
        by the config files for this, then the desired username can be
        fed in through the 'user' keyword argument.  This argument is
        ignored if its value is None."""

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
                print("Warning: Cannot import keyring module.", file=sys.stderr)
            else:
                password = keyring.get_password( self["keyring_service"],
                                                 user )
                if password is not None:
                    return password

        # We failed to get the password from the keyring, so prompt the
        # user for it
        password = getpass.getpass( "SR password: " )

        if self["use_keyring"] and keyring is not None:
            "Store password in the keyring"
            keyring.set_password( self["keyring_service"],
                                  user, password )

        return password
