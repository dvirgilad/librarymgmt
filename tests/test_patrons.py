"""Unit test for patrons"""
import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library, PatronNotFound
from patrons.patron_base import ProtectedAttribute


def test_add_teacher(test_library: Library):
    """Test adding a Teacher to the library"""
    test_teacher = Teacher(name="testTeacher", subject="test")
    add_teacher = test_library.add_patron(test_teacher)
    assert test_library.patrons[test_teacher.name] == test_teacher.category


def test_add_student(test_library: Library):
    """Test adding a Student to the library"""
    test_student = Student(name="testStudent", degree="test")
    add_student = test_library.add_patron(test_student)
    assert test_library.patrons[test_student.name] == test_student.category


def test_add_multiple_teachers_and_students(test_library: Library):
    """Test adding multiple patrons at once to the library"""
    test_teacher = Teacher(name="testTeacher", subject="test")
    test_student = Student(name="testStudent", degree="test")
    test_library.add_patrons([test_student, test_teacher])
    assert test_library.patrons[test_student.name] == test_student.category
    assert test_library.patrons[test_teacher.name] == test_teacher.category


def test_remove_patron(test_library_with_patrons: Library):
    """Test removing a patron from the library"""
    test_library_with_patrons.remove_patron("prePatron")
    assert "prePatron" not in test_library_with_patrons.patrons


def test_remove_patron_not_found(test_library_with_patrons: Library):
    """Test removing a patron that does not exist from the library"""
    with pytest.raises(PatronNotFound):
        test_library_with_patrons.remove_patron("prePatron3")


def test_edit_patron():
    """Test editing a patron"""
    to_edit = Teacher(name="steve", subject="math")
    to_edit.name = "bob"
    assert to_edit.name == "bob"


def test_edit_protected_patron_attribute():
    """Test editing the patron fines"""
    to_edit = Teacher(name="steve", subject="math")
    with pytest.raises(ProtectedAttribute):
        to_edit.fines = 500
