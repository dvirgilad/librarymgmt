from library_item.library_item_base import LibraryItem

import random


class Book(LibraryItem):
    def __init__(
        self, name: str, author: str, genre: str, fine: int, borrowing_period: int
    ):
        super().__init__(name, "book", fine, borrowing_period)
        self.author, self.genre = author, genre
        self.serial = random.randint(1, 1000)
