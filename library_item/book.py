from library_item.library_item_base import LibraryItem

import random
class Book(LibraryItem):
    def __init__(
        self,
        name: str,
        author: str,
        genre: str,
    ):
        super().__init__(name, "book")
        self.author, self.genre = author, genre
        self.serial = random.randint(1, 1000)

    def match_string(self, query):
        if (
            query.lower() in self.name.lower()
            or query.lower() in self.author.lower()
            or query.lower() in str(self.serial)
            or query.lower() in self.genre
        ):
            return True
        return False

