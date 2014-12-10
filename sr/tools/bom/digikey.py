"""Routines for scraping data about parts from digikey."""
from bs4 import BeautifulSoup
from decimal import Decimal
import re

from sr.tools.bom import distpart
from sr.tools.bom.cachedfetch import grab_url_cached


class Item(distpart.DistItem):
    """
    Represents a Digikey item.

    :param partNumber: The number of the part.
    """
    def __init__(self, partNumber):
        distpart.DistItem.__init__(self, partNumber)

        self.avail = 0
        self.min_order = 0
        self.price_for = 1
        self.multi = 1
        self.prices = []
        self.cost = []
        self.qty_range = 0

        page = grab_url_cached(
            'https://xgoat.com/p/digikey/' + str(partNumber))
        soup = BeautifulSoup(page)

        # Extract availability
        qa_heading = soup.find(text='Quantity Available')
        if qa_heading is None:
            raise distpart.NonExistentPart(self.part_number)

        qa = qa_heading.findNext('td').text
        qa = re.search("[1-9](?:\d{0,2})(?:,\d{3})*", qa)
        if qa is not None:
            qa = qa.group(0)
            self.avail = int(qa.replace(',', ''))
        else:
            self.avail = 0

        # Extract order multiple
        sp_heading = soup.find(text='Standard Package')
        self.multi = int(sp_heading.parent.findNext('td')
                         .contents[0].replace(',', ''))

        # Extract pricing
        # Get a list of the table rows, the first one is the heading row
        price_table = soup.find(text='Price Break').parent.parent.parent
        price_table_trs = price_table.findAll('tr')
        for row in price_table_trs:
            next_row = row.nextSibling.nextSibling
            # Skip first row as it contains headings, it does however give
            # access to the minimum quantity value on the next row.
            if row.find('th') is not None:
                self.min_order = int(next_row.contents[0].string.replace(',',
                                                                         ''))
                continue
            if next_row is not None:
                # Get top range of quantity from the next row
                qty = int(next_row.contents[0].string.replace(',', '')) - 1
            else:
                # For the last row just use its own quantity, there is no next
                # row.
                qty = int(row.contents[0].string.replace(',', ''))
            cost = Decimal(row.contents[1].string)
            self.prices.append((qty, cost))

    def get_info(self):
        """Return a dictionary of the info."""
        return dict(qty=self.qty_range,
                    price=self.cost,
                    num_for_price=self.price_for,
                    min_order=self.min_order,
                    multiple=self.multi,
                    number_available=self.avail)
