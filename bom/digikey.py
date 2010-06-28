"""Routines for scraping data about parts from digikey"""
from cachedfetch import grab_url_cached

class Item:
    """Represents a Digikey item"""

    def __init__(self, partNumber):
        self.avail = 0
        self.min_order = 0
        self.price_for = 1
        self.multi = 1
        self.prices = []
