"""Routines for extracting BOMs from schematics."""
from __future__ import print_function

from decimal import Decimal
import os

from sr.tools.bom import schem
from sr.tools.bom.threadpool import ThreadPool


STOCK_OUT = 0
STOCK_OK = 1
STOCK_UNKNOWN = 2

NUM_THREADS = 4


class PartGroup(list):
    """
    A set of parts. One might call this a "BOM line".

    :param part: The part.
    :param str name: The name of the group.
    :param list designators: A list of designators
    """
    def __init__(self, part, name="", designators=[]):
        """Create a new part group."""
        list.__init__(self)

        for x in designators:
            self.append((name, designators))

        self.part = part
        self.name = name

    def stockcheck(self):
        """
        Check the distributor has enough parts in stock.

        :returns: ``None`` if the result cannot be determined, ``True`` if the
                  distributor has enough parts, otherwise ``False``.
        :rtype: None or bool
        """
        s = self.part.stockcheck()
        if s is None:
            return None

        if s is True:
            # There are some in stock, but we don't know how many
            return None

        if s < self.order_num():
            return False
        return True

    def order_num(self):
        """
        Get the number of parts to order from a distributor.

        For example, if we need 5002 components from a 5000 component reel,
        this will return 2.

        :returns: The number of parts to order.
        :rtype: int
        """
        if self.part.stockcheck() is None:
            # unable to discover details from distributor...
            # assume one part per distributor unit
            return len(self)

        if self.part.get_dist_units() is None:
            # Same as above
            return len(self)

        n = len(self)
        if n == 0:
            return 0

        # change n to be in distributor units, rather than component units
        # (e.g. number of reels rather than number of components)
        d = n / self.part.get_dist_units()
        if n % self.part.get_dist_units() > 0:
            d = d + 1
        n = d

        if n < self.part.get_min_order():
            # round up to minimum order
            n = self.part.get_min_order()
        elif (n % self.part.get_increments()) != 0:
            n = n + (self.part.get_increments() -
                     (n % self.part.get_increments()))

        # Some (hopefully) sane assertions
        assert n % self.part.get_increments() == 0
        assert n >= self.part.get_min_order()

        return n

    def get_price(self):
        """
        Returns the price of the group.

        :returns: The price.
        :rtype: decimal.Decimal
        """
        n = self.order_num()

        p = self.part.get_price(n)
        if p is None:
            print("Warning: couldn't get price for %s (%s)" %
                  (self.part["sr-code"], self.part["supplier"]))
            return Decimal(0)

        return p * Decimal(n)


class Bom(dict):
    """A bill of materials."""
    def stockcheck(self):
        """
        Check that all items in the schematic are in stock.
        Returns list of things that aren't in stock.

        :returns: An iterator containing pairs of ``STOCK_UNKNOWN``,
                  ``STOCK_OUT``, ``STOCK_OK`` and the part.
        :rtype: iterator of tuples
        """
        for pg in self.values():
            a = pg.stockcheck()

            if a is None:
                yield (STOCK_UNKNOWN, pg.part)
            elif not a:
                yield (STOCK_OUT, pg.part)
            else:
                yield (STOCK_OK, pg.part)

    def get_price(self):
        """
        Get total price of all the items.

        :returns: The total price.
        :rtype: decimal.Decimal
        """
        tot = Decimal(0)
        for pg in self.values():
            tot = tot + pg.get_price()
        return tot


class BoardBom(Bom):
    """
    BOM object.
    Groups parts with the same asset code into PartGroups.
    Dictionary keys are asset codes.

    :param db: A parts DB instance.
    :param fname: The schematic to load from.
    :param name: The name to give the schematic.
    """
    def __init__(self, db, fname, name):
        """Create a new ``BoardBom`` object."""
        Bom.__init__(self)
        self.db = db
        self.name = name

        s = schem.open_schem(fname)

        for des, srcode in s.items():
            if srcode == "unknown":
                print("No value set for %s" % des)
                continue
            if srcode not in self:
                self[srcode] = PartGroup(db[srcode], name)
            self[srcode].append((name, des))


class MultiBoardBom(Bom):
    """
    A bill of materials with multiple boards.

    :param db: A parts DB instance."""
    def __init__(self, db):
        """Create multiple board BOM."""
        Bom.__init__(self)

        self.db = db

        # Array of 2-entry lists
        # 0: Number of boards
        # 1: Board
        self.boards = []

    def load_boards_args(self, args, allow_multipliers=True):
        """
        Load the BOM from board arguments, which is a list of arguments where
        each item is a string either starting with a '-' and then a number,
        meaning it is a multiplier, or just a string which contains the
        schematic.

        :param args: The board arguments.
        :param bool allow_multipliers: Whether or not to allow multipliers in
                                       the board arguments.
        """
        mul = 1

        for arg in args:
            if arg[0] == '-' and allow_multipliers:
                mul = int(arg[1:])
            else:
                board = BoardBom(self.db, arg, os.path.basename(arg))
                self.add_boards(board, mul)

    def add_boards(self, board, num):
        """
        Add boards to the collection.

        :param BoardCom board: The board to add.
        :param int num: The number of times to add it.
        """
        # already part of this collection?
        found = False
        for n in range(len(self.boards)):
            t = self.boards[n]
            if t[1] == board:
                t[0] = t[0] + num
                found = True
                break

        if not found:
            self.boards.append([num, board])

        # update our PartGroup dictionary
        self.clear()

        for num, board in self.boards:
            # Mmmmm. Horrible.
            for i in range(num):
                for srcode, bpg in board.items():
                    if srcode not in self:
                        self[srcode] = PartGroup(bpg.part)

                    self[srcode] += bpg

    def prime_cache(self):
        """
        Ensures that the webpage cache is filled in the quickest time possible
        by making many requests in parallel.
        """
        print("Getting data for parts from suppliers' websites")
        pool = ThreadPool(NUM_THREADS)

        for srcode, pg in self.items():
            print(srcode)
            pool.add_task(pg.get_price)

        pool.wait_completion()
