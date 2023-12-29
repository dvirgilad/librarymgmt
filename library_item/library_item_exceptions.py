from library.library_exceptions import AppException
from fastapi import status


class InvalidLibraryItem(AppException):
    """Exception raise if library item is invalid"""

    def __init__(self, item_id: str, message: str = None):
        self.item_id = item_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = (
            message or f"Library item with ID: {item_id} cannot be checked out"
        )
        super().__init__(self.status_code, self.message)


class LibraryItemNotFound(AppException):
    """Exception raised if library item not found in library"""

    def __init__(self, item_id: str, message: str = None):
        self.item_id = item_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message or f"Library item with ID: {item_id} not found"
        super().__init__(self.status_code, self.message)
