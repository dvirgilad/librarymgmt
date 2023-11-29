import abc


class Patron(abc.ABC):
    def __init__(self, category: str, fine_discount: int):
        self.category, self.items, self.fines, self.fine_discount = (
            category,
            [],
            0,
            fine_discount,
        )

    def update_patron(self, field: str, value):
        if hasattr(self, field.lower()) and field.lower() != "items":
            setattr(self, field.lower(), value)

    def get_fines(self):
        print(f"{self.category} Discount:")
        print(f"{self.name} has to pay ${self.fines * self.fine_discount} in FINES")
