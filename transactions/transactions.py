"""Transactions from library"""
import datetime
from enum import Enum
import csv
from beanie import Document
from typing import Literal
from library.library_dal import add_to_db
from library_item.dal.library_item_model import LibraryItemModel
from patrons.dal.patron_model import PatronModel


class Actions(Enum):
    """Action ENUM Class for logging"""

    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class TransactionModel(Document):
    patron: PatronModel
    library_item: LibraryItemModel
    action: Literal["BORROWED", "RETURNED"]
    timestamp: datetime.datetime


class Transaction:
    """Transaction class: Accepts name of library item, name of patron, and action"""

    def __init__(
        self,
        patron: PatronModel,
        library_item: LibraryItemModel,
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
            patron=patron,
            library_item=library_item,
            action=action,
            timestamp=timestamp,
        )

        def write_to_csv(self) -> None:
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

    async def send_log_to_db(self) -> str:
        """Send transaction log to mongo"""
        return str(await add_to_db(self.db_model))
