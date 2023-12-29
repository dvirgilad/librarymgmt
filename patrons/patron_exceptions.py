from library.library_exceptions import AppException
from fastapi import status


class PatronNotFound(AppException):
    """Exception raised if patron not found in library"""

    def __init__(self, patron_id: str, message: str = None):
        self.patron_id = (patron_id,)
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message or f"Patron with ID: {patron_id} not found"
        super().__init__(self.status_code, self.message)
