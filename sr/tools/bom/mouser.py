"""Routines for scraping data about parts from Mouser."""
from bs4 import BeautifulSoup
from decimal import Decimal as D
import re

from sr.tools.bom import distpart
from sr.tools.bom.cachedfetch import grab_url_cached


class Item(distpart.DistItem):
    """
    An item sold by Mouser.

    :param part_number: The number of the part.
    """
    def __init__(self, part_number):
        """Initialise a Mouser item."""
        distpart.DistItem.__init__(self, part_number)

        self._getinfo()

        # Not sure if this is a think with Mouser
        self.price_for = 1

    def _getinfo(self):
        """Load information from the distributor."""
        mouser_url = 'https://xgoat.com/p/mouser/{part_number}'
        page = grab_url_cached(mouser_url.format(part_number=self.part_number))

        soup = BeautifulSoup(page)

        if not self._check_exists(soup):
            raise distpart.NonExistentPart(self.part_number)

        # Check that the page we've been returned is for the requested part:
        if not self._soup_check_part(soup):
            raise distpart.NonExistentPart(self.part_number)

        self._get_availability(soup)

        # Only get pricing if it's not discontinued
        if self.avail is not None and not isinstance(self.avail, bool):
            self._get_pricing(soup)
            self._get_constraints(soup)

    def _check_exists(self, soup):
        """Work out whether the part exists based on the soup."""
        # Simple test: is this div present?
        if soup.find(attrs={"id": "product-details"}) is None:
            return False
        return True

    def _soup_check_part(self, soup):
        """Work out whether the info we've retrieved is for the right part."""
        sn = soup.find(attrs={"id": "divMouserPartNum"}).text.strip()
        return self.part_number == sn

    def _get_availability(self, soup):
        """Extract the part availability from the soup."""
        av = soup.find(attrs={"id": "ctl00_ContentMain_availability_tbl1"})
        av = av.find_all("td")[0]
        av = av.text.strip().replace(",", "")

        self.avail = int(av)

    def _get_pricing(self, soup):
        """Extract pricing information from the soup."""
        pt = soup.find(attrs={"id": "ctl00_ContentMain_divPricing"})

        prices = []

        # There are multiple rows with availability and prices in
        for row in pt.find("table").find_all("tr"):
            q = row.find(attrs={"class": "PriceBreakQuantity"})

            if q is not None:
                q = q.contents[1]
                qStr = q.string
                if qStr is None:
                    continue

                quantity = int(qStr.replace(",", ""))

                ps = row.find(attrs={"class": "PriceBreakPrice"}).contents[1]

                ps = ps.text

                try:
                    # The first character is a '£'
                    price = D(ps[1:])

                    prices.append((quantity, price))
                except:
                    # Sometimes Mouser say 'Quote'
                    pass

        if len(prices):
            # the minimum order is the smallest quantity from this table
            self.min_order = prices[0][0]

        self.prices = prices

    def _get_constraints(self, soup):
        """Extract the purchasing constraints from the soup."""

        av = soup.find("table", attrs={"id": "ctl00_ContentMain_tbl2"})

        av = av.find_all("tr")[1]
        av = av.find_all("td")[1]

        mo = re.search("\d", av.text).group(0)

        # mo now contains the minimum order quantity in string form
        self.min_order = int(mo)

        om = av.find("div")
        om = re.search("\d", om.text).group(0)

        # om now contains the order multiple in string form
        om = om.replace(",", "")
        self.multi = int(om)
