from library_item.library_item_base import LibraryItem
import random

class Disk(LibraryItem):
    def __init__(self, name: str, band: str, genre: str):
        super().__init__(name, "disk")
        self.band, self.genre = band, genre
        self.serial = random.randint(1001, 1999)

    def match_string(self, query):
        if (
            query.lower() in self.name.lower()
            or query.lower() in self.band.lower()
            or query.lower() in str(self.serial)
            or query.lower() in self.genre
        ):
            return True
        return False
