"""Unit tests of library items"""
from library_item.book import Book
from library_item.disk import Disk


def test_add_library_item(test_library):
    """Add a book to the library"""
    new_book = Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )
    add_book = test_library.add_item(new_book)
    assert add_book is True
    assert test_library.library_items[id(new_book)] == new_book


def test_add_multiple_library_item(test_library):
    """Test adding multiple library items to library"""
    new_book = Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )
    new_disk = Disk(
        name="MyDisk", band="Me", genre="Punk", fine=150, borrowing_period=30
    )
    add_library_items = test_library.add_items([new_book, new_disk])
    assert add_library_items is True
    assert len(test_library.library_items.keys()) == 2


# def test_remove_library_item(test_library_with_patrons_and_items):
#     remove_item = test_library_with_patrons_and_items.re


def test_update_library_item():
    """Test editing a library item"""
    to_edit = Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )
    edit_item = to_edit.update_item(attribute_to_edit="genre", new_value="SciFi")
    assert edit_item is True
    assert to_edit.genre == "SciFi"


def test_match_string():
    """Test searching for a string in a library item"""
    to_search = Book(
        name="MyBook", author="Me", genre="Horror", fine=150, borrowing_period=30
    )
    match_string = to_search.match_string("Me")
    assert match_string is True


def test_fail_match_string():
    """Test searching for a string that does not exist in a library item"""
    to_search = Disk(
        name="MyDisk", band="Me", genre="Punk", fine=150, borrowing_period=30
    )
    match_string = to_search.match_string("123123")
    assert match_string is False
