"""pytest fixtures for use in tests"""
import pytest
from patrons.student import Student
from patrons.teacher import Teacher
from library.library import Library


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
