"""Disk Class - inherits from the base library Item"""

from library_item.library_item_base import LibraryItem


class Disk(LibraryItem):
    """Disk class: Accepts a name, band, genre, borrowing period,
    and fine amount for each day late"""

    def __init__(
        self, name: str, band: str, genre: str, fine: int, borrowing_period: int
    ):
        super().__init__(name, "disk", fine, borrowing_period)
        self.band, self.genre = band, genre
