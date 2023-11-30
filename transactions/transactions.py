"""Transactions from library"""
from enum import Enum
import csv
import datetime


class Actions(Enum):
    """Action ENUM Class for logging"""

    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class Transaction:
    """Transaction class: Accepts name of library item, name of patron, and action"""

    def __init__(
        self, patron_name: str, item_name, action: Actions, timestamp: datetime.datetime
    ):
        self.patron_name, self.item_name, self.action, self.timestamp = (
            patron_name,
            item_name,
            action,
            timestamp,
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
