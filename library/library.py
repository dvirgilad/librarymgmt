"""Library Class. Handles Patrons and library items"""
from datetime import datetime

# from transactions.transactions import Transaction, Actions


class DeleteAttributeException(Exception):
    """Exception raised if there is an attempt to delete a protected attribute"""


class ProtectedAttribute(Exception):
    """If editing protected attribute"""


class Library:
    """Library class: accepts, name, list of patrons and dict of items with their ids"""

    def __init__(self, name, patrons: [], library_items: dict = None):
        self.name, self._patrons = name, []
