"""pytest fixtures for use in tests"""
import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library
from library_item.disk import Disk
from library_item.book import Book


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
def test_library_with_patrons_and_items():
    """library object preloaded with patrons for use in tests of editing/removing patrons"""
    new_book = Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )
    new_disk = Disk(
        name="MyDisk", band="Me", genre="Punk", fine=150, borrowing_period=30
    )
    return Library(
        "LIBWITEMS",
        [Student("prePatron", "test"), Teacher("PrePatron2", subject="test")],
        library_items={id(new_book): new_book, id(new_disk): new_disk},
    )
