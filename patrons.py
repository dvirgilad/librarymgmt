class Patron:
    def __init__(self, category: str):
        self.category, self.items, self.fines = category, [], 0

    def update_patron(self, field: str, value):
        if hasattr(self, field.lower()) and field.lower() != "items":
            setattr(self, field.lower(), value)

    def get_fines():
        pass


class Student(Patron):
    def __init__(self, name: str, degree: str):
        super().__init__("student")
        self.name, self.degree = name, degree

    def get_fines(self):
        print('Student Discount:')
        print(f"{self.name} has to pay ${self.fines * 0.8} in FINES")


class Teacher(Patron):
    def __init__(self, name: str, subject: str):
        super().__init__("teacher")
        self.name, self.subject = name, subject

    def get_fines(self):
        print('Employee Discount:')
        print(f"{self.name} has to pay ${self.fines * 0.5} in FINES")
