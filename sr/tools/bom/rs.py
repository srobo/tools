"""Routines for scraping data about parts from RS."""
from bs4 import BeautifulSoup
from decimal import Decimal as D

from sr.tools.bom import distpart
from sr.tools.bom.cachedfetch import grab_url_cached


class Item(distpart.DistItem):
    """
    An item sold by RS.

    :param part_number: The number of the part.
    """
    def __init__(self, part_number):
        """Initialise an RS item."""
        distpart.DistItem.__init__(self, part_number)

        self._getinfo()

        # Haven't come across an RS part for which this shouldn't be 1
        self.price_for = 1

        # This is not yet supported
        self.multi = 1

    def _getinfo(self):
        """Load information from the distributor."""
        rs_url = 'http://uk.rs-online.com/web/p/products/{part_number}/'
        page = grab_url_cached(rs_url.format(part_number=self.part_number))

        soup = BeautifulSoup(page)

        if not self._check_exists(soup):
            raise distpart.NonExistentPart(self.part_number)

        # Check that the page we've been returned is for the requested part:
        if not self._soup_check_part(soup):
            raise distpart.NonExistentPart

        self._get_availability(soup)

        # Only get pricing if it's not discontinued
        if self.avail:
            self._get_pricing(soup)

    def _check_exists(self, soup):
        """Work out whether the part exists based on the soup."""
        # Simple test: is this div present?
        if soup.find(attrs={"class": "keyDetailsDiv"}) is None:
            return False
        return True

    def _cmp_part_numbers(self, a, b):
        """Return True if the two part numbers are the same."""

        a = a.replace("-", "")
        b = b.replace("-", "")

        return a == b

    def _soup_check_part(self, soup):
        """Work out whether the info we've retrieved is for the right part."""

        # This div contains availability
        kd = soup.find(attrs={"class": "keyDetailsDiv"})

        # The label for the stock number field
        sl = kd.find(attrs={"class": "keyLabel"}, text="RS Stock No.")

        # And the value for that field
        sn = sl.find_next(attrs={"class": "keyValue"}).text

        return self._cmp_part_numbers(self.part_number, sn)

    def _get_availability(self, soup):
        """Extract the part availability from the soup."""

        av = soup.find(attrs={"class": "instockMessage"})

        if "In stock for next working day delivery" in av.text:
            self.avail = True
        elif "Discontinued" in av.text:
            self.avail = False
        else:
            self.avail = None

    def _get_pricing(self, soup):
        """Extract pricing information from the soup."""

        # The pricing table
        pt = soup.find(attrs={"class": "priceTable"})

        prices = []

        # There are multiple rows with availability and prices in
        for row in pt.find("tbody").find_all("tr"):

            quantity = int(row.find(attrs={"class": "quantity"}).text)

            ps = row.find(attrs={"class": "unitprice"}).text
            # The first character is a '£'
            price = D(ps[1:])

            prices.append((quantity, price))

        if len(prices):
            # the minimum order is the smallest quantity from this table
            self.min_order = prices[0][0]

        self.prices = prices
