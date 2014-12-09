"""
A set of classes and functions for working with
:doc:`The Inventory </inventory>`.
"""
from __future__ import print_function

import codecs
import email.utils
import hashlib
import re
import os
import subprocess
import sys

import six.moves.cPickle as pickle

import yaml

from sr.tools.inventory import assetcode
from sr.tools.environment import get_cache_dir


CACHE_DIR = get_cache_dir('inventory')
RE_PART = re.compile("^(.+)-sr([%s]+)$" % "".join(assetcode.alphabet_lut))


def find_top_level_dir(start_dir=None):
    """
    Find the top level of the inventory repo.

    :param str start_dir: The working to start the search from. If this is
                          None, the current working directory is used.
    :returns: The top level directory or None.
    :rtype: str or None
    """
    try:
        cmd = ['git', 'rev-parse', '--show-toplevel']
        gitdir = subprocess.check_output(cmd, universal_newlines=True,
                                         cwd=start_dir).strip()
    except subprocess.CalledProcessError:
        return None

    usersfn = os.path.join(gitdir, ".meta", "users")
    if not os.path.isfile(usersfn):
        return None

    return gitdir


def get_inventory(directory=None):
    """
    Get an :class:`Inventory` object for a directory.

    :param str directory: The directory to find the inventory from. If this is
                          left as None, the current working directory is used.
    :returns: An instance of an :class:`Inventory` object pointing to the
              inventory in the directory specified.
    :rtype: :class:`Inventory`
    :raises OSError: If the directory is not an inventory.
    """
    top = find_top_level_dir(directory)
    if top is None:
        raise OSError("Not an inventory.")

    return Inventory(top)


def should_ignore(path):
    """
    Check if the path should be ignored. A path that is deamed ignore-worthy
    starts with '.' or ends with '~'.

    :param str path: The path to check.
    :returns: ``True`` if the path should be ignored, else ``False``.
    :rtype: bool
    """
    if path[0] == ".":
        return True

    if path[-1] == "~":
        return True

    return False


def normalise_partcode(part_code):
    """
    Normalise the given part code to one that is compatible with the inventory
    API. Generally this just involves removing the 'sr' from the front and
    making the result all in uppercase.

    :param str part_code: The part code to normalise.
    :returns: A normalised part code.
    :rtype: str
    """
    part_code = part_code.strip()
    if part_code.lower().startswith('sr'):
        return part_code[2:].upper()
    else:
        return part_code.upper()


def cached_yaml_load(path):
    """
    Load a pickled YAML file from cache.

    :param str path: The path to load.
    :returns: The loaded YAML file, possibly from cache.
    :rtype: dict
    """
    path = os.path.abspath(path)

    ho = hashlib.sha256()
    ho.update(path.encode('UTF-8'))
    h = ho.hexdigest()

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    p = os.path.join(CACHE_DIR, h)
    if os.path.exists(p):
        # cache has file
        if os.path.getmtime(p) >= os.path.getmtime(path):
            # check that it's newer
            with open(p, 'rb') as file:
                return pickle.load(file)

    y = yaml.load(codecs.open(path, "r", encoding="utf-8"))
    with open(p, 'wb') as file:
        pickle.dump(y, file)
    return y


class Item(object):
    """An item in the inventory."""
    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        m = RE_PART.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load data from yaml file
        self.info_path = path
        self.info = cached_yaml_load(self.info_path)

        # Verify that assetcode matches filename
        if self.info["assetcode"] != self.code:
            print("Code in asset filename does not match contents of file:",
                  file=sys.stderr)
            print("\t code in filename: '%s'" % self.code, file=sys.stderr)
            print("\t code in contents: '%s'" % self.info["assetcode"],
                  file=sys.stderr)
            print("\n\tOffending file:", self.path, file=sys.stderr)
            exit(1)

        # The mandatory properties
        mand = ["labelled", "description", "value", "condition"]

        for pname in mand:
            try:
                setattr(self, pname, self.info[pname])
            except KeyError:
                raise Exception("Part sr{} is missing '{}' "
                                "property".format(self.code, pname))


class ItemTree(object):
    """A tree of items in the inventory."""
    def __init__(self, path, parent=None):
        self.name = os.path.basename(path)
        self.path = path
        self.parent = parent
        self.children = {}
        self._find_children()

        self.parts = {}
        self.types = {}
        for i in self.walk():
            self.parts[i.code] = i

            if i.name not in self.types:
                self.types[i.name] = []
            self.types[i.name].append(i)

    def _find_children(self):
        for fname in os.listdir(self.path):
            if should_ignore(fname) or fname == "info":
                # ignore dotfiles and group description files
                continue

            p = os.path.join(self.path, fname)

            if os.path.isfile(p):
                # it's got to be an item
                i = Item(p, parent=self)
                self.children[i.code] = i

            elif os.path.isdir(p):
                # could either be a group or a collection
                if RE_PART.match(p) is not None:
                    a = ItemGroup(p, parent=self)
                    self.children[a.code] = a
                else:
                    t = ItemTree(p, parent=self)
                    self.children[t.name] = t

    def walk(self):
        """Walk through the item tree."""
        for child in self.children.values():
            if hasattr(child, "walk"):
                for c in child.walk():
                    yield c

            if hasattr(child, "code"):
                yield child

    def resolve(self, path):
        "Resolve the given path into an object"
        if path[0] == "/":
            path = path[1:]

        pos = self
        for n in path.split("/"):
            pos = pos.children[n]

        return pos


class ItemGroup(ItemTree):
    "A group of items."
    def __init__(self, path, parent=None):
        ItemTree.__init__(self, path, parent=parent)

        m = RE_PART.match(os.path.basename(path))
        self.name = m.group(1)
        self.code = m.group(2)

        # Load info from 'info' file
        self.info_path = os.path.join(path, "info")
        self.info = cached_yaml_load(self.info_path)

        if self.info["assetcode"] != self.code:
            print("Code in group directory name does not match info file:",
                  file=sys.stderr)
            print("\t code in directory name: '%s'" % self.code,
                  file=sys.stderr)
            print("\t           code in info: '%s'" % self.info["assetcode"],
                  file=sys.stderr)
            print("\n\tOffending group:", self.path, file=sys.stderr)
            sys.exit(1)

        self.description = self.info["description"]

        if "elements" not in self.info:
            raise Exception("Group %s lacks an elements field" % self.code)

        self.elements = self.info["elements"]


class Inventory(object):
    """An inventory."""
    def __init__(self, root_path):
        self.root_path = root_path
        self.root = ItemTree(root_path)

        self._load_users()

    def _load_users(self):
        self.users = {}

        with open(os.path.join(self.root_path, '.meta', 'users')) as file:
            users = yaml.safe_load(file)

        for details, user_id in users.items():
            self.users[email.utils.parseaddr(details)] = user_id

    @property
    def current_user_id(self):
        """
        Get the user ID of the currently configure Git user.
        """
        user = self.get_current_user()
        return self.users[user]

    @staticmethod
    def get_current_user():
        """
        Get the currently configured Git user.

        :returns: A tuple containing the name and email address.
        :rtype: tuple
        """
        gitname = subprocess.check_output(("git", "config", "user.name")).strip()
        gitemail = subprocess.check_output(("git", "config", "user.email")).strip()
        return (gitname.decode('UTF-8'), gitemail.decode('UTF-8'))

    def query(self, query_str):
        """
        Run a query on the inventory.

        :param str query_str: The query to run on the inventory.
        :returns: Any items found from the query.
        :rtype: list of :class:`Item`s
        :raises pyparsing.ParseError: If the query could not be parsed.
        """
        from sr.tools.inventory import query_parser  # circular dependency

        tree = query_parser.search_tree(query_str)
        return tree.match(self.root.parts.values())
