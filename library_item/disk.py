from library_item.library_item_base import LibraryItem
import random


class Disk(LibraryItem):
    def __init__(
        self, name: str, band: str, genre: str, fine: int, borrowing_period: int
    ):
        super().__init__(name, "disk", fine, borrowing_period)
        self.band, self.genre = band, genre
        self.serial = random.randint(1001, 1999)
