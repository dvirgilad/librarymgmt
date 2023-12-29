"""Generic exceptions"""
from fastapi import status


class AppException(Exception):
    """Base exception class"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class DeleteAttributeException(AppException):
    """Exception raised if there is an attempt to delete a protected attribute"""

    def __init__(self, object_id: str, attribute: str, message: str = None):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message or f"Cannot delete {attribute}"
        super().__init__(self.status_code, self.message)


class ProtectedAttribute(AppException):
    """If editing protected attribute"""

    def __init__(self, object_id: str, attribute: str, message: str = None):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message or f"Cannot edit {attribute}"
        super().__init__(self.status_code, self.message)


class InvalidID(AppException):
    """Raised if searching for invalid object ID"""

    def __init__(self, object_id: str, message: str = None):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message if message else f"{object_id} is not a valid object ID"
        super().__init__(self.status_code, self.message)
