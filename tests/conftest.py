"""pytest fixtures for use in tests"""
import mongomock
import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from mongoengine import connect

from library_item.library_item_model import LibraryItemBase, LibraryItemModel
from main import app
from patrons.dal.patron_model import PatronCreate, PatronEdit, PatronReturn
from patrons.dal.patron_document import PatronModel
from consts import EXAMPLE_OBJECT_ID


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
    return PatronCreate(
        name="testTeacher",
        category="TEACHER",
        fine_discount=1.5,
        fines=0,
    )


@pytest.fixture
def save_patron_then_delete(test_student_document):
    test_student_document.save()
    yield
    test_student_document.delete()


@pytest.fixture
def test_edit_patron_basemodel():
    return PatronEdit(name="edited")


@pytest.fixture
def test_student_basemodel():
    return PatronCreate(
        id=EXAMPLE_OBJECT_ID,
        name="testStudent",
        category="STUDENT",
        fine_discount=15,
        fines=0,
        degree="Testing",
    )


@pytest.fixture
def test_student_return_basemodel():
    return PatronReturn(
        id=EXAMPLE_OBJECT_ID,
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
def test_teacher_document():
    return PatronModel(
        name="testTeacher",
        category="TEACHER",
        patron_attributes={"subject": "testing"},
        fines=0,
        fine_discount=0,
    )


@pytest.fixture
def add_multiple_patrons_then_delete(test_student_document, test_teacher_document):
    test_student_document.save()
    test_teacher_document.save()
    yield
    test_student_document.delete()
    test_teacher_document.delete()


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
