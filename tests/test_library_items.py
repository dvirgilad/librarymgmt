"""Unit tests of library items"""
import pytest
from library_item.library_item_controller import *
from transactions.transactions import Transaction


def test_add_library_item(mocker, test_book_basemodel, test_book_document):
    """Add a book to the library"""
    mocker.patch.object(
        LibraryItemModelFactory, "create_model", return_value=test_book_document
    )
    mocker.patch("library_item.library_item_controller.add_to_db", return_value="12345")
    mocker.patch(
        "library_item.library_item_controller.check_if_borrowed", return_value=False
    )
    book_id = create_library_item(test_book_basemodel)
    assert book_id == "12345"


def test_remove_library_item(mocker, test_book_basemodel, test_book_document):
    """Test removing an item from the library"""
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_document,
    )
    mocker.patch(
        "library_item.library_item_controller.check_if_borrowed", return_value=False
    )
    mock_delete = mocker.patch(
        "library_item.library_item_controller.remove_from_db", return_value=None
    )

    remove_library_item(test_book_basemodel)
    mock_delete.assert_called_once_with(test_book_document)


def test_update_library_item(mocker, test_book_document):
    """Test editing a library item"""
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_document,
    )
    mock_edit = mocker.patch(
        "library_item.library_item_controller.update_libray_items_info_in_db",
        return_value=None,
    )
    update_library_item("12345", "genre", "scifi")
    mock_edit.assert_called_once_with(test_book_document, "genre", "scifi")


def test_get_library_item(mocker, test_book_basemodel, test_book_document):
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_document,
    )
    mocker.patch.object(
        LibraryItemModelFactory, "create_basemodel", return_value=test_book_basemodel
    )

    test_model = get_library_item("12345")
    assert test_model == test_book_basemodel


def test_check_if_borrowed_false(test_book_document):
    test_check = check_if_borrowed(test_book_document)
    assert test_check is False


def test_model_factory_create_model(test_book_basemodel, test_book_document):
    new_model = LibraryItemModelFactory().create_model(test_book_basemodel)
    assert type(new_model) == LibraryItemModel
    assert new_model["name"] == test_book_document["name"]


def test_get_library_item_from_db(mocker, test_book_document):
    test_book_document.save()
    get_item = get_library_item_from_db(test_book_document.id)
    assert get_item.to_json() == test_book_document.to_json()
    ## Have to delete library items for other tests because data persists between tests
    test_book_document.delete()


def test_get_all_library_items_from_db(mocker):
    test_book_model = LibraryItemModel(name="test")
    test_book_model.save()
    test_disk_model = LibraryItemModel(name="test2")
    test_disk_model.save()
    all_items = get_all_library_items_from_db(2, 0)
    assert [library_item.id for library_item in all_items] == [
        test_book_model.id,
        test_disk_model.id,
    ]
    test_book_model.delete()
    test_disk_model.delete()


def test_update_library_item_in_db(mocker):
    test_book_model = LibraryItemModel(name="test")
    test_book_model.save()
    update_libray_items_info_in_db(test_book_model, "name", "updated")
    assert test_book_model.name == "updated"
    test_book_model.delete()


def test_borrow_item(mocker, test_book_document, test_student_document):
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_document,
    )
    mocker.patch(
        "library_item.library_item_controller.search_for_patron",
        return_value=test_student_document,
    )
    mocker.patch(
        "library_item.library_item_controller.check_if_borrowed", return_value=False
    )
    mocker.patch(
        "library_item.library_item_controller.update_libray_items_info_in_db",
        return_value=None,
    )
    mocker.patch.object(Transaction, "send_log_to_db", return_value="789")
    transaction_id = borrow_item("123", "456")
    assert transaction_id == "789"


def test_return(mocker, test_book_document, test_student_document):
    test_book_document.borrower = test_student_document
    test_book_document.borrowed_status = True
    test_book_document.borrowed_at = datetime.utcnow()
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_document,
    )
    mocker.patch(
        "library_item.library_item_controller.check_if_borrowed", return_value=True
    )
    mocker.patch(
        "library_item.library_item_controller.check_if_returned_late", return_value=True
    )
    mocker.patch(
        "library_item.library_item_controller.update_libray_items_info_in_db",
        return_value=None,
    )
    mocker.patch(
        "library_item.library_item_controller.update_patron_info_in_db",
        return_value=None,
    )
    mocker.patch.object(Transaction, "send_log_to_db", return_value="789")
    transaction_id = return_library_item("123")
    assert transaction_id == "789"


def test_search_library_items_in_db():
    # cannot test beacause text indexes are not implemented in mongomock
    # test_book_document.save()
    # search_response = search_library_items_in_db("test")
    # assert search_response == [test_book_document]
    pass


def test_search_library_items(mocker, test_book_document, test_book_basemodel):
    mocker.patch(
        "library_item.library_item_controller.search_library_items_in_db",
        return_value=[test_book_document],
    )
    mocker.patch.object(
        LibraryItemModelFactory, "create_basemodel", return_value=test_book_basemodel
    )
    test_search = search_library_items("test", 1, 0)
    assert test_search == [test_book_basemodel]


def test_get_library_item_route(mocker, client, test_book_basemodel):
    mocker.patch(
        "library_item.library_item_routes.get_library_item",
        return_value=test_book_basemodel,
    )
    model_json = test_book_basemodel.model_dump()
    test_response = client.get("/items/12345")
    assert test_response.status_code == 200
    assert test_response.json()["name"] == model_json["name"]


def test_get_all_library_items_route(mocker, client, test_book_basemodel):
    mocker.patch(
        "library_item.library_item_routes.get_all_library_items",
        return_value=[test_book_basemodel.model_dump_json()],
    )
    test_response = client.get("/items")
    assert test_response.status_code == 200
    assert len(test_response.json()["items"]) == 1


def test_update_library_item_route(mocker, client):
    mock_patch = mocker.patch(
        "library_item.library_item_routes.update_library_item",
        return_value=None,
    )
    response = client.patch("/items/12345?attribute_to_edit=name&new_value=test")
    mock_patch.assert_called_once_with("12345", "name", "test")
    assert response.status_code == 200


def test_remove_library_item_route(mocker, client):
    mock_delete = mocker.patch(
        "library_item.library_item_routes.remove_library_item",
        return_value=None,
    )
    response = client.delete("/items/12345")
    mock_delete.assert_called_once_with("12345")
    assert response.status_code == 200
