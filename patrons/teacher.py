"""Teacher Class - inherits from the base Patron class"""
from patrons.patron_base import Patron, PatronTypes
from patrons.patron_model import TeacherModel


class Teacher(Patron):
    """Teacher class: Accepts a name and subject. The fine discount is 50%"""

    def __init__(self, name: str, subject: str):
        teacher_fine_discount = 0.5
        super().__init__(
            name, PatronTypes.TEACHER.value, fine_discount=teacher_fine_discount
        )
        self.subject = subject
        self.db_model = TeacherModel(
            name=name,
            category=PatronTypes.TEACHER.value,
            subject=subject,
            fines=self.fines,
            discount=self.fine_discount,
        )
