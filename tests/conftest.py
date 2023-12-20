"""pytest fixtures for use in tests"""
import pytest
from fastapi.testclient import TestClient
from patrons.patron_model import PatronBase, Patron, PatronModel
from library_item.library_item_model import (
    LibraryItem,
    LibraryItemBase,
    LibraryItemModel,
)
from main import app
from bson import ObjectId

import mongomock
from mongoengine import connect, disconnect


def pytest_configure(config):
    """Initialize connection to mock DB"""
    connect(
        "mongoenginetest",
        host="mongodb://localhost:27017",
        mongo_client_class=mongomock.MongoClient,
    )


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_teacher_basemodel():
    return PatronBase(
        name="testTeacher",
        category="TEACHER",
        fine_discount=1.5,
        fines=0,
    )


@pytest.fixture
def test_student_basemodel():
    return PatronBase(
        name="testStudent",
        category="STUDENT",
        fine_discount=15,
        fines=0,
        degree="Testing",
    )


@pytest.fixture
def test_book_basemodel():
    return LibraryItemBase(
        _id=ObjectId(),
        name="TestBook1",
        fine=100,
        borrowing_period=100,
        author="ME",
        genre="testing",
        category="BOOK",
    )


@pytest.fixture
def test_student_document():
    return PatronModel(
        name="teststudent",
        category="STUDENT",
        patron_attributes={"degree": "testing"},
        fines=0,
        fine_discount=0,
    )


@pytest.fixture
def test_book_document():
    return LibraryItemModel(
        name="TestBook1",
        fine=100,
        borrowing_period=100,
        author="ME",
        genre="testing",
        borrower=None,
        category="BOOK",
    )
