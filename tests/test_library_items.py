"""Unit tests of library items"""
from library_item.library_item_controller import *
from consts import EXAMPLE_OBJECT_ID, SUCCESSFUL_HTTP_CODE
import pytest


@pytest.mark.asyncio
async def test_add_library_item(mocker, test_book_basemodel):
    """Add a book to the library"""
    mocker.patch(
        "library_item.library_item_controller.LibraryItemModel",
        return_value=test_book_basemodel,
    )
    mocker.patch(
        "library_item.library_item_controller.add_to_db", return_value=EXAMPLE_OBJECT_ID
    )
    book_id = await create_library_item(test_book_basemodel)
    assert book_id == EXAMPLE_OBJECT_ID


@pytest.mark.asyncio
async def test_remove_library_item(mocker, test_book_basemodel):
    """Test removing an item from the library"""
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_basemodel,
    )
    mocker.patch(
        "library_item.library_item_controller.check_if_borrowed", return_value=False
    )
    mock_delete = mocker.patch(
        "library_item.library_item_controller.remove_from_db", return_value=None
    )

    await remove_library_item(EXAMPLE_OBJECT_ID)
    mock_delete.assert_called_once_with(test_book_basemodel)


@pytest.mark.asyncio
async def test_update_library_item(
    mocker, test_book_basemodel, test_edit_library_item_model
):
    """Test editing a library item"""
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_basemodel,
    )
    mock_edit = mocker.patch(
        "library_item.library_item_controller.update_libray_items_info_in_db",
        return_value=None,
    )
    await update_library_item(EXAMPLE_OBJECT_ID, test_edit_library_item_model)
    mock_edit.assert_called_once_with(
        test_book_basemodel,
        **test_edit_library_item_model.model_dump(exclude_none=True),
    )


@pytest.mark.asyncio
async def test_get_library_item(mocker, test_book_basemodel):
    mocker.patch(
        "library_item.library_item_controller.search_for_library_item_by_id",
        return_value=test_book_basemodel,
    )

    test_model = await get_library_item(EXAMPLE_OBJECT_ID)
    assert test_model == test_book_basemodel.model_dump()


# @pytest.mark.asyncio
# async def test_check_if_borrowed_false(test_book_document):
#     test_check = await check_if_borrowed(test_book_document)
#     assert test_check is False

# CANT TEST BECAUSE CAN'T ADD DOCUMENTS
# @pytest.mark.asyncio
# async def test_borrow_item(mocker, test_book_basemodel, test_student_basemodel):
#     mocker.patch(
#         "library_item.library_item_controller.search_for_library_item_by_id",
#         return_value=test_book_basemodel,
#     )
#     mocker.patch(
#         "library_item.library_item_controller.search_for_patron",
#         return_value=test_student_basemodel,
#     )
#     mocker.patch(
#         "library_item.library_item_controller.check_if_borrowed", return_value=False
#     )
#     mocker.patch(
#         "library_item.library_item_controller.update_libray_items_info_in_db",
#         return_value=None,
#     )
#     mocker.patch.object(Transaction, "send_log_to_db", return_value=EXAMPLE_OBJECT_ID)
#     transaction_id = await borrow_item(EXAMPLE_OBJECT_ID, EXAMPLE_OBJECT_ID)
#     assert transaction_id == EXAMPLE_OBJECT_ID


# @pytest.mark.asyncio
# async def test_return(mocker, test_book_document, test_student_document):
#     test_book_document.borrower = test_student_document
#     test_book_document.borrowed_status = True
#     test_book_document.borrowed_at = datetime.utcnow()
#     mocker.patch(
#         "library_item.library_item_controller.search_for_library_item_by_id",
#         return_value=test_book_document,
#     )
#     mocker.patch(
#         "library_item.library_item_controller.check_if_borrowed", return_value=True
#     )
#     mocker.patch(
#         "library_item.library_item_controller.check_fine_amount", return_value=True
#     )
#     mocker.patch(
#         "library_item.library_item_controller.update_libray_items_info_in_db",
#         return_value=None,
#     )
#     mocker.patch(
#         "library_item.library_item_controller.update_patron_info_in_db",
#         return_value=None,
#     )
#     mocker.patch.object(Transaction, "send_log_to_db", return_value="789")
#     transaction_id = await return_library_item("123")
#     assert transaction_id == "789"


@pytest.mark.asyncio
async def test_search_library_items_in_db():
    # cannot test beacause text indexes are not implemented in mongomock
    # test_book_document.save()
    # search_response = search_library_items_in_db("test")
    # assert search_response == [test_book_document]
    pass


@pytest.mark.asyncio
async def test_search_library_items(mocker, test_book_basemodel):
    mocker.patch(
        "library_item.library_item_controller.search_library_items_in_db",
        return_value=[test_book_basemodel],
    )
    test_search = await search_library_items("test", 1, 0)
    assert test_search["items"] == [test_book_basemodel]


@pytest.mark.asyncio
async def test_get_library_item_route(
    mocker, client, test_add_library_item_return_model
):
    mocker.patch(
        "library_item.library_item_routes.get_library_item",
        return_value=test_add_library_item_return_model,
    )
    test_response = client.get(f"/items/{EXAMPLE_OBJECT_ID}")
    assert test_response.status_code == SUCCESSFUL_HTTP_CODE
    assert (
        test_response.json()["name"]
        == test_add_library_item_return_model.model_dump()["name"]
    )


@pytest.mark.asyncio
async def test_get_all_library_items_route(
    mocker, client, test_add_library_item_return_model
):
    mocker.patch(
        "library_item.library_item_routes.get_all_library_items",
        return_value={"items": test_add_library_item_return_model.model_dump()},
    )
    test_response = client.get("/items")
    assert test_response.status_code == 200
    assert (
        test_response.json()["items"]["name"] == test_add_library_item_return_model.name
    )


@pytest.mark.asyncio
async def test_update_library_item_route(mocker, client, test_edit_library_item_model):
    model_dict = test_edit_library_item_model.model_dump(exclude_none=True)
    mock_patch = mocker.patch(
        "library_item.library_item_routes.update_library_item",
        return_value=None,
    )
    response = client.patch(f"/items/{EXAMPLE_OBJECT_ID}", json=model_dict)
    mock_patch.assert_called_once_with(EXAMPLE_OBJECT_ID, test_edit_library_item_model)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_remove_library_item_route(mocker, client):
    mock_delete = mocker.patch(
        "library_item.library_item_routes.remove_library_item",
        return_value=None,
    )
    response = client.delete("/items/12345")
    mock_delete.assert_called_once_with("12345")
    assert response.status_code == 200
