# -*- coding: utf-8 -*-
"""Routines for scraping data about parts from Farnell"""
from bs4 import BeautifulSoup
import distpart
from cachedfetch import grab_url_cached
from decimal import Decimal as D
import re

class Item(distpart.DistItem):
    def __init__(self, part_number):
        distpart.DistItem.__init__(self, part_number)

        self._get_data()

    def _get_data(self):
        page = grab_url_cached( 'https://xgoat.com/p/farnell/{0}'.format(self.part_number) )

        soup = BeautifulSoup(page)

        # Check that it exists
        if not self._check_exists(soup):
            raise distpart.NonExistentPart( self.part_number )

        # Check that the part we've retrieved is the requested part:
        if not self._soup_check_part(soup):
            raise distpart.NonExistentPart( self.part_number )

        self._get_availability(soup)

        if self.avail != None and not isinstance(self.avail, bool):
            self._get_pricing(soup)
            self._get_constraints(soup)

    def _check_exists(self, soup):
        "Determine if the part exists from the soup"

        # This div seems to exist on part pages, but not others
        if soup.find( attrs = { "class": "order-details" } ) == None:
            return False
        return True

    def _soup_get_pddict(self, soup):
        "Return a dict of the part details table information"

        pd = soup.find( "dl", attrs = {"class": "pd_details" } )

        details = {}

        for dt in pd.find_all( "dt" ):
            key = dt.text.strip()
            if key == "":
                continue

            val = dt.find_next("dd").text.strip()
            details[key] = val

        return details
    
    def _soup_check_part(self, soup):
        "Check the part in the soup is the one we wanted"
        details = self._soup_get_pddict(soup)
        return details["Order Code:"] == self.part_number

    def _get_availability(self, soup):
        "Extract the part availability from the soup"

        av = soup.find( "div", attrs = {"class": "availability"} )
        sd = av.find( attrs = {"class": "stockDetail"} )

        if sd != None:
            stock = sd.find("b").text
        else:
            "Some parts have a different format"

            sd = av.find( attrs = {"class": "prodDetailAvailability"} )

            stock = sd.find( attrs = {"class": "stockDetails"} )

            if stock == None:
                "The stockDetails tag disappears in this situation"

                if sd.find( text = re.compile(".*Awaiting Delivery.*") ) != None:
                    stock = "0"
                elif sd.find( text = re.compile( ".*Out of Stock.*") ) != None:
                    stock = "0"
                else:
                    raise distpart.UnsupportedFormat( self.part_number )
            else:
                stock = stock.text

        # They put commas in their numbers
        stock = stock.replace( ",", "" )

        self.avail = int(stock)

    def _parse_quantity(self, q):
        "Parse a quantity string, return the lower boundary"
        if "-" in q:
            return int( q.split("-")[0].strip() )
        elif "+" in q:
            return int( q.split("+")[0].strip() )
        else:
            raise distpart.UnsupportedFormat( self.part_number )

    def _get_pricing(self, soup):
        "Extract the item pricing from the soup"

        # The table of quantities and prices
        pd = soup.find( id = "otherquantites" )

        prices = []

        for row in pd.find_all( "tr" )[1:]:

            cells = row.find_all("td")

            quant_str = cells[0].text.strip()
            if quant_str == "":
                continue

            q = self._parse_quantity( quant_str )
            p = D( cells[1].text.strip()[1:] )

            prices.append( (q,p) )

        self.prices = prices

    def _get_constraints(self, soup):
        "Extract the purchasing constraints from the soup"

        av = soup.find( "div", attrs = {"class": "availability"} )

        # The "Price For" row
        pf = av.find( text = re.compile( ".*Price For.*" ) ) \
            .parent.next_sibling.strip()

        # pf now contains a string like "1 each" or "Reel of 5,000"
        e = re.search( "([0-9,]+)", pf ).group(1)
        e = e.replace( ",", "" )
        self.price_for = D(e)

        # The minimum order quantity row
        mo = av.find( text = re.compile( ".*Minimum Order Quantity.*" ) ) \
            .parent.next_sibling.strip()

        # mo now contains the minimum order quantity in string form
        mo = mo.replace( ",", "" )
        self.min_order = int(mo)

        # The order multiple row
        om = av.find( text = re.compile( ".*Order Multiple.*" ) ) \
            .parent.next_sibling.strip()

        # om now contains the order multiple in string form
        om = om.replace( ",", "" )
        self.multi = int(om)
