"""pytest fixtures for use in tests"""
import pytest
from patrons.student import Student
from patrons.patron_model import TeacherBase, StudentBase, StudentModel
from patrons.teacher import Teacher
from library_item.library_item_model import BookBase, BookModel

# from library.library import Library
from datetime import datetime
import mongomock
from mongoengine import connect, disconnect
from pytest import Config


def pytest_configure(config):
    """Initialize connection to mock DB"""
    connect(
        "mongoenginetest",
        host="mongodb://localhost:27017",
        mongo_client_class=mongomock.MongoClient,
    )


# @pytest.fixture
# def test_library():
#     """empty library object for use in tests"""
#     return Library("TESTLIB", [])


# @pytest.fixture
# def test_library_with_patrons():
#     """library object preloaded with patrons for use in tests of editing/removing patrons"""
#     return Library(
#         "LIBWPATRONS",
#         [Student("prePatron", "test"), Teacher("PrePatron2", subject="test")],
#     )


# @pytest.fixture
# def test_book():
#     """Book object for testing"""
#     return Book(
#         name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
#     )


@pytest.fixture
def test_teacher_basemodel():
    return TeacherBase(
        name="testTeacher",
        category="TEACHER",
        fine_discount=1.5,
        fines=0,
        subject="Testing",
    )


@pytest.fixture
def test_student_basemodel():
    return StudentBase(
        name="testStudent",
        category="STUDENT",
        fine_discount=15,
        fines=0,
        degree="Testing",
    )


@pytest.fixture
def test_book_basemodel():
    return BookBase(
        name="TestBook1",
        fine=100,
        borrowing_period=100,
        author="ME",
        genre="testing",
    )


@pytest.fixture
def test_student_document():
    return StudentModel(
        name="teststudent", category="STUDENT", degree="testing", fines=0
    )


@pytest.fixture
def test_book_document():
    return BookModel(
        name="TestBook1",
        fine=100,
        borrowing_period=100,
        author="ME",
        genre="testing",
        borrower=None,
        category="BOOK",
    )


# @pytest.fixture
# def test_teacher():
#     """Teacher object for testing"""
#     return Teacher("PrePatron2", subject="test")


# @pytest.fixture
# def test_library_with_patrons_and_items(test_book, test_teacher):
#     """library object preloaded with patrons for use in tests of editing/removing patrons"""

#     new_disk = Disk(
#         name="MyDisk", band="Me", genre="Punk", fine=150, borrowing_period=30
#     )
#     return Library(
#         "LIBWITEMS",
#         [Student("prePatron", "test"), test_teacher],
#         library_items={id(test_book): test_book, id(new_disk): new_disk},
#     )


# @pytest.fixture
# def test_borrowed_item(test_teacher):
#     """borrow a book"""
#     book = Book(
#         name="borrowedBook", author="me", genre="Fantasy", fine=100, borrowing_period=10
#     )
#     book.borrowed_status = True
#     book._borrower = test_teacher
#     book.time_borrowed = datetime.now()
#     return book


# @pytest.fixture
# def library_with_borrowed_item(test_borrowed_item, test_teacher):
#     """library with borrowed item and patron"""
#     return Library(
#         name="BorrowedItemLib",
#         patrons=[test_teacher],
#         library_items={id(test_borrowed_item): test_borrowed_item},
#     )
