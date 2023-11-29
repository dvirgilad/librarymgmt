"""Base Patron class"""
import abc


class Patron(abc.ABC):
    """Base patron class: accepts name, category(student/teacher/...) and a fine discount"""

    def __init__(self, name: str, category: str, fine_discount: int):
        self.name, self.category, self.items, self.fines, self.fine_discount = (
            name,
            category,
            [],
            0,
            fine_discount,
        )

    def update_patron(self, field: str, value) -> bool:
        """Updates the valid fields of a patron"""

        if hasattr(self, field.lower()) and field.lower() != "items":
            setattr(self, field.lower(), value)
        return True

    def get_fines(self) -> float:
        """Returns how much money a patron has accrued"""
        print(f"{self.category} Discount:")
        print(f"{self.name} has to pay ${self.fines * self.fine_discount} in FINES")
        return self.fines * self.fine_discount
