"""Teacher Class - inherits from the base Patron class"""
from patrons.patron_base import Patron, PatronTypes
from patrons.patron_model import TeacherModel


class Teacher(Patron):
    """Teacher class: Accepts a name and subject. The fine discount is 50%"""

    def __init__(self, name: str, subject: str):
        teacher_fine_discount = 0.5
        super().__init__(
            name, PatronTypes.TEACHER.name, fine_discount=teacher_fine_discount
        )
        self.subject = subject
