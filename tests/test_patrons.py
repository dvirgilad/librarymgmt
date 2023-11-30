"""Unit test for patrons"""
import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library
from patrons.patron_base import LoweringFinesException


def test_add_teacher(test_library: Library):
    """Test adding a Teacher to the library"""
    test_teacher = Teacher(name="testTeacher", subject="test")
    add_teacher = test_library.add_patron(test_teacher)
    assert add_teacher is True
    assert test_library.patrons == [test_teacher]


def test_add_student(test_library: Library):
    """Test adding a Student to the library"""
    test_student = Student(name="testStudent", degree="test")
    add_student = test_library.add_patron(test_student)
    assert add_student is True
    assert test_library.patrons == [test_student]


def test_add_multiple_teachers_and_students(test_library: Library):
    """Test adding multiple patrons at once to the library"""
    test_teacher = Teacher(name="testTeacher", subject="test")
    test_student = Student(name="testStudent", degree="test")
    add_patrons = test_library.add_patrons([test_student, test_teacher])
    assert add_patrons is True
    assert test_library.patrons == [test_student, test_teacher]


def test_remove_patron(test_library_with_patrons: Library):
    """Test removing a patron from the library"""
    remove_patron = test_library_with_patrons.remove_patron("prePatron")
    assert remove_patron is True
    assert test_library_with_patrons.patrons[0].name == "PrePatron2"


def test_remove_patron_not_found(test_library_with_patrons: Library):
    """Test removing a patron that does not exist from the library"""
    remove_patron = test_library_with_patrons.remove_patron("prePatron3")
    assert remove_patron is False


def test_edit_patron():
    """Test editing a patron"""
    to_edit = Teacher(name="steve", subject="math")
    to_edit.name = "bob"
    assert to_edit.name == "bob"


def test_edit_protected_patron_attribute():
    """Test editing the patron fines"""
    to_edit = Teacher(name="steve", subject="math")
    with pytest.raises(LoweringFinesException):
        to_edit.fines = 500
