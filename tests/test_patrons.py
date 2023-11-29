import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library


def test_add_teacher(test_library: Library):
    test_teacher = Teacher(name="testTeacher", subject="test")
    add_teacher = test_library.add_patron(test_teacher)
    assert add_teacher is True
    assert test_library.patrons == [test_teacher]


def test_add_student(test_library: Library):
    test_student = Student(name="testStudent", degree="test")
    add_student = test_library.add_patron(test_student)
    assert add_student is True
    assert test_library.patrons == [test_student]


def test_add_multiple_teachers_and_students(test_library: Library):
    test_teacher = Teacher(name="testTeacher", subject="test")
    test_student = Student(name="testStudent", degree="test")
    add_patrons = test_library.add_patrons([test_student, test_teacher])
    assert add_patrons is True
    assert test_library.patrons == [test_student, test_teacher]


def test_remove_patron(test_library_with_patrons: Library):
    remove_patron = test_library_with_patrons.remove_patron("prePatron")
    assert remove_patron is True
    assert test_library_with_patrons.patrons[0].name == "PrePatron2"


def test_remove_patron_not_found(test_library_with_patrons: Library):
    remove_patron = test_library_with_patrons.remove_patron("prePatron3")
    assert remove_patron is False
