"""Disk Class - inherits from the base library Item"""
from library_item.library_item_model import DiskModel
from library_item.library_item_base import LibraryItem, LibraryItemTypes


class Disk(LibraryItem):
    """Disk class: Accepts a name, band, genre, borrowing period,
    and fine amount for each day late"""

    def __init__(
        self, name: str, band: str, genre: str, fine: int, borrowing_period: int
    ):
        super().__init__(name, LibraryItemTypes.DISK.value, fine, borrowing_period)
        self.band, self.genre = band, genre
        self.db_model = DiskModel(
            name=name,
            band=band,
            genre=genre,
            fine=fine,
            borrowing_period=borrowing_period,
            borrowed_status=False,
        )
