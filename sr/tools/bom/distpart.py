"""Superclass for distributor items."""
from __future__ import print_function


class NonExistentPart(Exception):
    """The part does not exist."""
    pass


class UnsupportedFormat(Exception):
    "The page returned by the distributor was of an unsupported format"
    pass


class DistItem(object):
    """
    A distributor item.

    :param part_number: The part number of the item.
    """
    def __init__(self, part_number):
        """Create a new distributor item."""
        self.part_number = part_number

        # The number of items currently available
        # None <- Unknown
        # False <- Discontinued -- i.e. never going to be available
        # True <- Some in stock, but we don't know how many
        # [int] <- The number that are in stock
        self.avail = None

        # The minimum number of this item that one can order
        # (None <- Unknown)
        self.min_order = None

        # The number of components per item
        # e.g. for an item that's a 5000 component reel, this
        # number is 5000.
        # (None <- Unknown)
        self.price_for = None

        # The smallest quantity increment that one can make
        # (None <- Unknown)
        self.multi = None

        # List of prices
        # 2-entry tuples -- (quantity, unit price)
        self.prices = None

    def print_info(self):
        """Print all information about the part."""
        print("Part", self.part_number)

        print("\tStock:", end="")
        if self.avail is None:
            print("Unknown")
        elif isinstance(self.avail, bool) and self.avail is False:
            print("Discontinued")
        elif self.avail is True:
            print("In stock")
        else:
            print("%i in stock" % self.avail)

        def f(n):
            if n is None:
                return "Unknown"
            else:
                return n

        print("\tMinimum order:", f(self.min_order))

        print("\tComponents per item:", f(self.price_for))

        print("\tOrder multiple:", f(self.multi))

        print("\tPricing:")

        if self.prices is None:
            print("\t\tUnknown")
        else:
            for i in range(0, len(self.prices)):
                quantity, price = self.prices[i]

                if i + 1 < len(self.prices):
                    n_quant = self.prices[i + 1][0]

                    print("\t\t %i - %i: £%s" %
                          (quantity, n_quant - self.multi, price))
                else:
                    print("\t\t %i+: £%s" % (quantity, price))
