"""Library for accessing the budget files."""
from __future__ import print_function

import collections
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR, ROUND_UP
import runpy
import os
import six
from subprocess import check_call, check_output, CalledProcessError
import sys
import tempfile
from tempfile import NamedTemporaryFile
import tokenize

from six.moves import cStringIO as StringIO
import yaml

try:
    from yaml import CLoader as YAML_Loader
except ImportError:
    from yaml import Loader as YAML_Loader


# Spending against a budget line is allowed to go over its value by this factor
FUDGE_FACTOR = D("1.1")


def dict_constructor(loader, node):
    """Constructor for libyaml to use ordered dicts instead of dicts."""
    return collections.OrderedDict(loader.construct_pairs(node))


def num_constructor(loader, node):
    """Constructor for libyaml to translate numeric literals to Decimals."""
    return D(node.value)


# Give me ordered dictionaries back
YAML_Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                            dict_constructor)

# Parse floats as decimals
YAML_Loader.add_constructor("tag:yaml.org,2002:float", num_constructor)


def dec_ceil(d):
    """Get the ceiling of a decimal."""
    return d.to_integral_exact(ROUND_CEILING)


def dec_floor(d):
    """Get the floor of a decimal."""
    return d.to_integral_exact(ROUND_FLOOR)


def py_translate_to_decimals(s):
    """Translate any literal floats in the given source into decimals."""

    # Parse numbers in the string as Decimals
    # based on example from http://docs.python.org/2.7/library/tokenize.html
    result = []
    g = tokenize.generate_tokens(StringIO(str(s)).readline)
    for toknum, tokval, _, _, _ in g:
        if toknum == tokenize.NUMBER and '.' in tokval:
            result.extend([
                (tokenize.NAME, 'Decimal'),
                (tokenize.OP, '('),
                (tokenize.STRING, repr(tokval)),
                (tokenize.OP, ')')
            ])
        else:
            result.append((toknum, tokval))

    # Turn it back into python
    return tokenize.untokenize(result)


class BudgetItem(object):
    """
    A budget item.

    :param str name: The name of the item.
    :param str fname: The filename of the item.
    :param conf: The configuration."""
    def __init__(self, name, fname, conf):
        """Create a new budget item."""
        self.fname = fname
        self.conf = conf
        y = yaml.load(open(fname, "r"), Loader=YAML_Loader)

        if False in [x in y for x in ["cost", "summary", "description"]]:
            print("Error: %s does not match schema." % fname, file=sys.stderr)
            sys.exit(1)

        self.name = name
        self.summary = y["summary"]
        self.description = y["description"]

        if "closed" in y:
            self.closed = y["closed"]
        else:
            self.closed = False

        if self.closed:
            # Lines that are closed have no uncertainty
            self.uncertainty = 0
        elif "uncertainty" in y:
            self.uncertainty = D(y["uncertainty"])
        else:
            self.uncertainty = FUDGE_FACTOR - 1

        if "consumable" in y:
            self.consumable = y["consumable"]
        else:
            self.consumable = None

        self.cost = self._parse_cost(y["cost"], conf)

    def _parse_cost(self, s, conf):
        """Parse the cost string."""
        s = py_translate_to_decimals(s)
        cost = eval(s,
                    {"Decimal": D,
                     "ceil": dec_ceil,
                     "ceiling": dec_ceil,
                     "floor": dec_floor},
                    conf.vars)

        if isinstance(cost, int):
            cost = D(cost)

        # Round the result up to the nearest penny
        cost = cost.quantize(D("0.01"), rounding=ROUND_UP)

        return cost


class InvalidPath(Exception):
    """An exception representing an invalid budget path."""
    pass


class BudgetTree(object):
    """
    Container for the BudgetItems and BudgetTrees below a certain point.

    :param str name: The name of the tree.
    """
    def __init__(self, name):
        """Create the budget tree."""
        self.children = {}
        self.name = name

    def add_child(self, child):
        """
        Add a child to the tree.

        :param child: The child to add.
        :type child: ``BudgetTree`` or ``BudgetItem``.
        :raises ValueError: If the child is not a valid type.
        """
        if isinstance(child, BudgetTree):
            self.children[child.name] = child
        elif isinstance(child, BudgetItem):
            self.children[os.path.basename(child.name)] = child
        else:
            raise ValueError("Attempted to add unsupported object type to "
                             "BudgetTree")

    def total(self):
        """
        Sum all children.

        :returns: The total cost of all the children.
        :rtype: decimal.Decimal
        """
        t = D(0)
        for ent in self.children.values():
            if isinstance(ent, BudgetTree):
                t += ent.total()
            else:
                t += ent.cost
        return t

    def walk(self):
        """
        Walk through all the BudgetItems of the this tree.

        :returns: An iterator over the items in the tree.
        """
        for c in self.children.values():
            if isinstance(c, BudgetItem):
                yield c
            elif isinstance(c, BudgetTree):
                for e in c.walk():
                    yield e

    def path(self, path):
        """
        Get the object at the given path relative to this one.

        :returns: The object at the path.
        :raises InvalidPath: If the path is invalid.
        """
        pos = self
        for s in path.split("/"):
            try:
                pos = pos.children[s]
            except KeyError:
                raise InvalidPath("'{}' has no child node '{}'"
                                  .format(pos.name, s))
        return pos

    def draw(self, fd=sys.stdout, space="  ", prefix=""):
        """
        Draw a text-representation of the tree.

        :param fd: Where to print the result.
        :param space: The string representing a space.
        :param prefix: The prefix for each line in the tree.
        """
        format_string = '{prefix}--{name} ({cost})'
        print(format_string.format(prefix=prefix,
                                   name=os.path.basename(self.name),
                                   cost=self.total()), file=fd)

        for n, c in enumerate(self.children.values()):
            child_prefix = prefix + space

            if isinstance(c, BudgetItem):
                if n == len(self.children) - 1:
                    child_prefix += "+"
                else:
                    child_prefix += "|"

                print(format_string.format(prefix=child_prefix,
                                           name=os.path.basename(c.name),
                                           cost=c.cost), file=fd)

            elif isinstance(c, BudgetTree):
                child_prefix = prefix + space

                if n == len(self.children) - 1:
                    child_prefix += " "
                else:
                    child_prefix += "|"

                c.draw(fd=fd, prefix=child_prefix)


class NoBudgetConfig(Exception):
    """
    An exception representing that no config file for the budget has been
    found.
    """
    def __init__(self):
        super(NoBudgetConfig, self).__init__("No config file found")


class BudgetConfig(object):
    """
    A class representing a budget config.

    :param str root: The root path to the budget.
    """
    def __init__(self, root):
        """Create a new budget config."""
        pypath = os.path.join(root, "config.py")
        yamlpath = os.path.join(root, "config.yaml")

        if os.path.exists(pypath):
            self._load_from_py(pypath)
            self.path = pypath
        elif os.path.exists(yamlpath):
            self._load_from_yaml(yamlpath)
            self.path = yamlpath
        else:
            raise NoBudgetConfig()

    def _load_from_py(self, fname):
        with open(fname, "r") as in_file:
            in_src = in_file.read()

        if six.PY3:
            tempfile = NamedTemporaryFile('w', encoding='utf-8')
        else:
            tempfile = NamedTemporaryFile('w')

        with tempfile as f:
            trans_src = py_translate_to_decimals(in_src)
            f.write(trans_src)
            f.flush()

            conf = runpy.run_path(f.name,
                                  init_globals={"Decimal": D,
                                                "ceil": dec_ceil,
                                                "ceiling": dec_ceil,
                                                "floor": dec_floor})

        # Variables that are part of the normal running environment
        nullset = set(runpy.run_path("/dev/null").keys())

        # Remove vars that are part of the normal running env
        for name in nullset:
            if name in conf:
                conf.pop(name)

        self.vars = conf

        for vname in list(self.vars.keys()):
            val = self.vars[vname]
            if type(val) not in [int, D, float]:
                self.vars.pop(vname)

    def _load_from_yaml(self, fname):
        """Munge the old yaml file into a python file."""
        # Use the python loader to make ordered dicts work
        y = yaml.load(open(fname, "r"), Loader=YAML_Loader)

        if six.PY3:
            tempfile = NamedTemporaryFile('w', encoding='utf-8')
        else:
            tempfile = NamedTemporaryFile('w')

        with tempfile as f:
            for vname, val in y["vars"].items():
                print("{0} = {1}".format(vname, val), file=f)

            f.flush()
            self._load_from_py(f.name)


def load_budget(root):
    """
    Load the budget from a budget root.

    :param root: The root path to the budget.
    """
    root = os.path.abspath(root)
    funds_in_path = os.path.join(root, "funds-in.yaml")
    conf = BudgetConfig(root)
    tree = BudgetTree("sr")

    for dirpath, dirnames, filenames in os.walk(root):
        for d in [".git", ".meta"]:
            try:
                dirnames.remove(d)
            except ValueError:
                # those directories will not always be there
                pass

        for fname in filenames:
            fullp = os.path.abspath(os.path.join(dirpath, fname))
            if fullp in [conf.path, funds_in_path]:
                # these files are yaml files, but not budget items
                continue

            if fname[-5:] != ".yaml":
                continue

            name = fullp[len(root) + 1:-5]

            r = tree
            for d in name.split("/")[:-1]:
                if d not in r.children:
                    r.add_child(BudgetTree(d))

                r = r.children[d]

            r.add_child(BudgetItem(name, fullp, conf))
    return tree


class TmpBudgetExport(object):
    """
    A class for temporarily exporting a budget.

    :param root: The root path to the budget.
    :param rev: The revision to export.
    """
    def __init__(self, root, rev):
        """Create a new temporary budget export."""
        self.rev = rev
        self.tmpdir = tempfile.mkdtemp()

        self._export(root, rev, self.tmpdir)
        self.btree = load_budget(self.tmpdir)

    def _export(self, root, rev, path):
        check_call("git archive {0} | tar -x -C {1}".format(rev, path),
                   cwd=root, shell=True)


def load_budget_rev(root, rev):
    """
    Load a specific revision of the budget.

    :param str root: The root of the budget.
    :param str rev: The revision to get.
    """
    t = TmpBudgetExport(root, rev)
    return t.btree


class NotBudgetRepo(Exception):
    """An exception raised if the repo is not a budget."""
    pass


def find_root(path=None):
    """
    Find the root directory of the budget repository.

    Checks that the repository is budget.git too.

    :param path: if provided is a path within the budget.git repository
                 (defaults to working directory)
    """
    if path is None:
        path = os.getcwd()

    try:
        # check that we're in budget.git

        with open("/dev/null", "w") as n:
            check_call(["git", "rev-list",
                        # This is the first commit of spending.git
                        "c7e8a3bdc82ad244ed302bf9a7f4934e0ca83292"],
                       cwd=path,
                       stdout=n,
                       stderr=n)
    except CalledProcessError:
        # it's not the spending repository
        raise NotBudgetRepo()

    root = check_output(["git", "rev-parse", "--show-toplevel"],
                        cwd=path)

    return root.strip().decode('utf-8')


class AddedItem(object):
    """An item that has been added to the budget."""
    def __init__(self, a):
        self.a = a


class RemovedItem(object):
    """An item that has been removed from the budget."""
    def __init__(self, a):
        self.a = a


class ChangedItem(object):
    """An item in the budget that has been changed."""
    def __init__(self, a, b):
        self.a = a
        self.b = b


def _item_dict(tree):
    items = {}
    for i in tree.walk():
        items[i.name] = i

    return items


def diff_trees(a, b):
    """
    Get the difference betwen two budget trees.

    :returns: A sorted list of changes containing either ``AddedItem``,
              ``RemovedItem`` or ``ChangedItem`` objects.
    :rtype: list of ``AddedItem``, ``RemovedItem`` and ``ChangedItem``
    """
    a_items = _item_dict(a)
    b_items = _item_dict(b)

    # Remove items from this list as we find them
    # it'll eventually have things in it that aren't in A
    added = list(b_items.values())

    changes = []

    for ai in a_items.values():
        if ai.name in b_items:
            # Features in both trees
            bi = b_items[ai.name]
            added.remove(bi)

            if bi.cost != ai.cost:
                # changed value
                changes.append(ChangedItem(ai, bi))
        else:
            # it's been removed
            changes.append(RemovedItem(ai))

    for i in added:
        changes.append(AddedItem(i))

    return sorted(changes, key=lambda change: change.a.name)


def changes_to_tree(changes):
    """
    Convert a list of changes into a tree.

    :param changes: A list of changes in the budget.
    :raises ValueError: If the list of changes contains non-change objects.
    :returns: A new budget tree.
    :rtype: BudgetTree
    """
    tree = BudgetTree("sr")

    for c in changes:
        item = None

        if isinstance(c, AddedItem):
            item = c.a
        elif isinstance(c, ChangedItem):
            # Craft a new item that describes the change in cost
            item = BudgetItem(c.a.name, c.a.fname, c.a.conf)
            item.cost = c.b.cost - c.a.cost
        elif isinstance(c, RemovedItem):
            # Craft a new item that describes the reduction in cost
            item = BudgetItem(c.a.name, c.a.fname, c.a.conf)
            item.cost *= -1
        else:
            raise ValueError("Unsupported object type in change list")

        def fudge_parent(parents, name):
            """Fudge a directory name in because there were two..."""
            name = "{0}.d".format(name)
            if name in parents[-1].children:
                res = parents[-1].children[name]
            else:
                res = BudgetTree(name)
                parents[-1].add_child(res)

            return res

        r = tree
        parents = []

        for d in item.name.split("/")[:-1]:

            if not hasattr(r, "children"):
                # It's not a directory:
                # Add a directory at the same level with '.d' on the end.
                r = fudge_parent(parents, d)

            if d not in r.children:
                r.add_child(BudgetTree(d))

            parents.append(r)
            r = r.children[d]

        if not isinstance(r, BudgetTree):
            # need to fudge a directory in
            r = fudge_parent(parents, os.path.basename(r.name))

        if os.path.basename(item.name) in r.children:
            raise ValueError("Unsupported situation!")

        r.add_child(item)

    return tree
