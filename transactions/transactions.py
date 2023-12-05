"""Transactions from library"""
from enum import Enum
import csv
import datetime
from mongoengine import Document, StringField, DateField, ReferenceField
from library_item.library_item_model import LibraryItemModel
from patrons.patron_model import PatronModel
from library_item.library_item_base import LibraryItem
from patrons.patron_base import Patron


class Actions(Enum):
    """Action ENUM Class for logging"""

    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class TransactionModel(Document):
    patron = ReferenceField(PatronModel)
    library_item = ReferenceField(LibraryItemModel)
    action = StringField()
    timestamp = DateField()


class Transaction:
    """Transaction class: Accepts name of library item, name of patron, and action"""

    def __init__(
        self,
        patron: Patron,
        library_item: LibraryItem,
        action: Actions,
        timestamp: datetime.datetime,
    ):
        self.patron_name, self.item_name, self.action, self.timestamp = (
            patron.name,
            library_item.name,
            action,
            timestamp,
        )
        self.db_model = TransactionModel(
            patron=patron.db_model,
            library_item=library_item.db_model,
            action=action,
            timestamp=timestamp,
        )

    def send_to_csv(self) -> None:
        """Write Library transaction to transaction.csv"""
        with open("transactions.csv", "a", newline="", encoding="UTF-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(
                [
                    str(self.timestamp),
                    self.patron_name,
                    self.action,
                    self.item_name,
                ]
            )

    def send_to_mongo(self) -> None:
        """Send transaction log to mongo"""
        self.db_model.save()
