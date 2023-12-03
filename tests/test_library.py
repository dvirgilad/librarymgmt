import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library


def test_search_library(test_library_with_patrons_and_items, test_book):
    """Test searching the library for a string"""
    search_for_book = test_library_with_patrons_and_items.search_library("MyBook")
    assert search_for_book == [test_book]


def test_borrow(test_library_with_patrons_and_items, test_book, test_teacher):
    test_library_with_patrons_and_items.borrow_item(test_book, test_teacher)
    assert test_book.borrower == test_teacher


def test_return_item(test_borrowed_item, library_with_borrowed_item):
    print(test_borrowed_item)
    library_with_borrowed_item.return_item(item_to_return=test_borrowed_item)
    assert test_borrowed_item.borrower is None
