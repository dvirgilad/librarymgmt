"""Teacher Class - inherits from the base Patron class"""
from patrons.patron_base import Patron


class Teacher(Patron):
    """Teacher class: Accepts a name and subject. The fine discount is 50%"""

    def __init__(self, name: str, subject: str):
        super().__init__(name, "teacher", fine_discount=0.5)
        self.subject = subject
