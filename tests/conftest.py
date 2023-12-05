"""pytest fixtures for use in tests"""
import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library
from library_item.disk import Disk
from library_item.book import Book
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


@pytest.fixture
def test_library():
    """empty library object for use in tests"""
    return Library("TESTLIB", [])


@pytest.fixture
def test_library_with_patrons():
    """library object preloaded with patrons for use in tests of editing/removing patrons"""
    return Library(
        "LIBWPATRONS",
        [Student("prePatron", "test"), Teacher("PrePatron2", subject="test")],
    )


@pytest.fixture
def test_book():
    """Book object for testing"""
    return Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )


@pytest.fixture
def test_teacher():
    """Teacher object for testing"""
    return Teacher("PrePatron2", subject="test")


@pytest.fixture
def test_library_with_patrons_and_items(test_book, test_teacher):
    """library object preloaded with patrons for use in tests of editing/removing patrons"""

    new_disk = Disk(
        name="MyDisk", band="Me", genre="Punk", fine=150, borrowing_period=30
    )
    return Library(
        "LIBWITEMS",
        [Student("prePatron", "test"), test_teacher],
        library_items={id(test_book): test_book, id(new_disk): new_disk},
    )


@pytest.fixture
def test_borrowed_item(test_teacher):
    """borrow a book"""
    book = Book(
        name="borrowedBook", author="me", genre="Fantasy", fine=100, borrowing_period=10
    )
    book.borrowed_status = True
    book._borrower = test_teacher
    book.time_borrowed = datetime.now()
    return book


@pytest.fixture
def library_with_borrowed_item(test_borrowed_item, test_teacher):
    """library with borrowed item and patron"""
    return Library(
        name="BorrowedItemLib",
        patrons=[test_teacher],
        library_items={id(test_borrowed_item): test_borrowed_item},
    )
