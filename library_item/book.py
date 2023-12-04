"""Book Class - inherits from the base library Item"""
from library_item.library_item_base import LibraryItem, LibraryItemTypes
from library_item.library_item_model import BookModel


class Book(LibraryItem):
    """Book class: Accepts a name, author, genre, borrowing period, and fine amount per day"""

    def __init__(
        self, name: str, author: str, genre: str, fine: int, borrowing_period: int
    ):
        super().__init__(name, LibraryItemTypes.BOOK.value, fine, borrowing_period)
        self.author, self.genre = author, genre
        self.db_model = BookModel(
            name=name,
            author=author,
            genre=genre,
            fine=fine,
            borrowing_period=borrowing_period,
            borrowed_status=False,
        )
