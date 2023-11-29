import abc

class Patron(abc.ABC):
    def __init__(self, category: str):
        self.category, self.items, self.fines = category, [], 0

    def update_patron(self, field: str, value):
        if hasattr(self, field.lower()) and field.lower() != "items":
            setattr(self, field.lower(), value)
    @abc.abstractmethod
    def get_fines():
        pass

