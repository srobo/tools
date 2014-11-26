import fnmatch

from sr.tools.inventory import inventory
from functools import reduce


class ASTNode(object):
    pass


class NonTerminal(ASTNode):

    def match(self, inv_nodes):
        raise NotImplementedError("match(...) not implemented"
                                  " for {}".format(self.__class__))


class Terminal(ASTNode):

    def match_single(self, inv_node):
        raise NotImplementedError("match_single(...) not implemented"
                                  " for {}".format(self.__class__))

    def match(self, inv_nodes):
        return filter(self.match_single, inv_nodes)


class Not(NonTerminal):

    def __init__(self, node):
        super(Not, self).__init__()
        self.node = node

    def match(self, inv_nodes):
        matches = self.node.match(inv_nodes)
        return list(set([x for x in inv_nodes if x not in matches]))

    def sexpr(self):
        return "(NOT {0})".format(self.node.sexpr())


class And(NonTerminal):

    def __init__(self, left, right):
        super(And, self).__init__()
        self.left = left
        self.right = right

    def match(self, inv_nodes):
        left_matches = self.left.match(inv_nodes)
        right_matches = self.right.match(inv_nodes)
        return list({x for x in inv_nodes
                     if (x in left_matches and x in right_matches)})

    def sexpr(self):
        return "(AND {0} {1})".format(self.left.sexpr(), self.right.sexpr())


class Or(NonTerminal):

    def __init__(self, left, right):
        super(Or, self).__init__()
        self.left = left
        self.right = right

    def match(self, inv_nodes):
        left_matches = self.left.match(inv_nodes)
        right_matches = self.right.match(inv_nodes)
        return list({x for x in inv_nodes
                     if (x in left_matches or x in right_matches)})

    def sexpr(self):
        return "(OR {0} {1})".format(self.left.sexpr(), self.right.sexpr())


class Condition(Terminal):

    def __init__(self, *conditions):
        super(Condition, self).__init__()
        self.conditions = set(conditions)

    def _flatten(self, l):
        if type(l) not in (list, tuple):
            return l
        ret = []
        for i in l:
            if type(i) in (list, tuple):
                ret.extend(self._flatten(i))
            else:
                ret.append(i)
        return ret

    def _state(self, inv_node):
        if isinstance(inv_node, inventory.Item):
            return inv_node.condition

        elif isinstance(inv_node, inventory.ItemGroup):
            expected = inv_node.elements
            if expected is None:
                return 'working'
            ret = []
            for name in expected:
                count = 1
                if isinstance(name, dict):
                    count = name.values()[0]
                    name = name.keys()[0]
                if name not in inv_node.types:
                    ret.append('broken')
                if name in inv_node.types:
                    c = 0
                    for type_ in inv_node.types[name]:
                        if c == count:
                            break
                        ret.append(self._state(type_))
                        c += 1
                    if c != count:
                        ret.append('broken')
                else:
                    ret.append('broken')
            ret = set(self._flatten(ret))
            if len(ret) == 1:
                return ret.pop()
            if 'broken' in ret:
                return 'broken'
            return 'unknown'

    def match_single(self, inv_node):
        return self._state(inv_node) in self.conditions

    def sexpr(self):
        return "(Condition {0})".format(list(self.conditions))


class Type(Terminal):

    def __init__(self, *types):
        super(Type, self).__init__()
        self.types = types

    def match_single(self, inv_node):
        if hasattr(inv_node, 'name'):
            for type in self.types:
                if fnmatch.fnmatch(inv_node.name, type):
                    return True
        return False

    def sexpr(self):
        return "(Type {0})".format(list(self.types))


class Labelled(Terminal):

    def __init__(self, labelled):
        super(Labelled, self).__init__()
        self.labelled = labelled.lower() in ('true', '1')

    def match_single(self, inv_node):
        if hasattr(inv_node, 'labelled'):
            return inv_node.labelled == self.labelled
        return False

    def sexpr(self):
        return "(Labelled {0})".format(self.labelled)


class Assy(Terminal):

    def __init__(self, assy):
        super(Assy, self).__init__()
        self.assy = assy.lower() in ('true', '1')

    def match_single(self, inv_node):
        return self.assy == (hasattr(inv_node, 'code')
                             and hasattr(inv_node, 'children'))

    def sexpr(self):
        return "(Assy {0})".format(self.assy)


class TriState(Terminal):

    def __init__(self, key, desired_val):
        super(TriState, self).__init__()
        self.key = key
        self.desired_val = desired_val.lower()

    def match_single(self, inv_node):
        if self.desired_val == 'unset':
            return self.key not in inv_node.info.keys()
        if self.key in inv_node.info.keys():
            if self.desired_val == "true":
                return inv_node.info[self.key]
            else:
                return inv_node.info[self.key] is False
        return False

    def sexpr(self):
        return "(TriState {0}: {1})".format(self.key, self.desired_val)


class Path(Terminal):

    def __init__(self, *paths):
        super(Path, self).__init__()
        paths = [path[1:] if path[0] == '/' else path for path in paths]
        self.paths = [path + '*' for path in paths]

    def _root_path(self, inv_node):
        n = inv_node
        while n is not None:
            if n.parent is None:
                return n.path
            n = n.parent

    def match_single(self, inv_node):
        root_path = self._root_path(inv_node)
        if hasattr(inv_node, 'path'):
            for path in self.paths:
                if fnmatch.fnmatch(inv_node.path[len(root_path) + 1:], path):
                    return True
        return False

    def sexpr(self):
        return "(Path {0})".format(list(self.paths))


class Code(Terminal):

    def __init__(self, *codes):
        self.codes = set(map(self._tidy, codes))

    def _tidy(self, code):
        code = code.upper()
        if code.startswith('SR'):
            code = code[2:]
        return code

    def match_single(self, inv_node):
        return inv_node.code in self.codes

    def sexpr(self):
        return "(Code {0})".format(list(self.codes))


class Serial(Terminal):

    def __init__(self, *serials):
        self.serials = set(serials)

    def match_single(self, inv_node):
        serial = inv_node.info.get("serial", None)
        return serial in self.serials

    def sexpr(self):
        return "(Serial {0})".format(list(self.serials))


class Function(NonTerminal):

    _functions = {}

    @classmethod
    def register(cls, name):
        def wrap(f):
            cls._functions[name] = f
            return f
        return wrap

    @classmethod
    def registered_names(cls):
        return cls._functions.keys()

    def __init__(self, func_name, node):
        self.func_name = func_name
        self.node = node

    def match(self, inv_nodes):
        return list(set(reduce(lambda x, y: list(x) + list(y),
                               map(self._functions[self.func_name],
                                   self.node.match(inv_nodes)), [])))

    def sexpr(self):
        return "(Function '{0}' {1})".format(self.func_name, self.node.sexpr())


@Function.register('parent')
def _parent(inv_node):
    return [inv_node.parent]


@Function.register('children')
def _children(inv_node):
    if not hasattr(inv_node, 'children'):
        return []
    return inv_node.children.values()


@Function.register('siblings')
def _siblings(inv_node):
    return [x for x in inv_node.parent.children.values() \
              if x is not inv_node]


@Function.register('descendants')
def _descendants(inv_node):
    def rec(node):
        children = getattr(node, 'children', {})
        return sum(map(rec, children.values()), [node])
    return rec(inv_node)[1:]
