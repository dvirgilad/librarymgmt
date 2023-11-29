"""Base Library Item """
import abc


class LibraryItem(abc.ABC):
    """Base Library Class: accepts name, item type fine and borrowing period"""

    def __init__(
        self,
        name,
        item_type,
        fine,
        borrowing_period,
    ):
        self.name, self.type, self.fine, self.borrowing_period, self.borrowed_status = (
            name,
            item_type,
            fine,
            borrowing_period,
            False,
        )

    def update_item(self, attribute_to_edit, new_value):
        """Change valid attributes of a library item"""
        for item_attribute in vars(self).keys():
            if item_attribute.lower() == attribute_to_edit.lower():
                setattr(self, item_attribute, new_value)
                return True
        return False

    def match_string(self, query) -> bool:
        """Check if query string matches any attribute of item for search"""
        for value in vars(self).values():
            if query.lower() in str(value).lower():
                return True
