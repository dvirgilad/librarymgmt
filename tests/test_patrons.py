"""Unit test for patrons"""
import pytest
from patrons.patron_controller import (
    PatronNotFound,
    create_patron,
    PatronModelFactory,
    search_for_patron,
    remove_patron,
    update_patron,
)
from patrons.dal.patron_dal import (
    get_all_patrons_from_db,
    get_patron_from_db,
    update_patron_info_in_db,
)

from consts import SUCCESSFUL_HTTP_CODE, EXAMPLE_OBJECT_ID


def test_add_teacher(mocker, test_teacher_basemodel):
    mocker.patch.object(
        PatronModelFactory, "create_model", return_value=test_teacher_basemodel
    )
    mocker.patch("patrons.patron_controller.add_to_db", return_value=EXAMPLE_OBJECT_ID)
    test_id = create_patron(test_teacher_basemodel)
    assert test_id == EXAMPLE_OBJECT_ID


def test_add_student(mocker, test_student_basemodel):
    mocker.patch.object(
        PatronModelFactory, "create_model", return_value=test_student_basemodel
    )
    mocker.patch("patrons.patron_controller.add_to_db", return_value=EXAMPLE_OBJECT_ID)
    test_id = create_patron(test_student_basemodel)
    assert test_id == EXAMPLE_OBJECT_ID


def test_remove_patron(mocker):
    """Test removing a patron from the library"""
    mocker.patch(
        "patrons.patron_controller.search_for_patron", return_value={"name": "example"}
    )
    patch_remove = mocker.patch(
        "patrons.patron_controller.remove_from_db", return_value=None
    )
    remove_patron(EXAMPLE_OBJECT_ID)
    patch_remove.assert_called_once_with({"name": "example"})


def test_searching_for_patron(mocker, test_teacher_basemodel):
    """test searching for patron that does exist"""
    mocker.patch(
        "patrons.patron_controller.get_patron_from_db",
        return_value=test_teacher_basemodel,
    )
    get_patron = search_for_patron("DoesNotExist")
    assert get_patron == test_teacher_basemodel


def test_search_for_patron_not_found(mocker):
    """test searching for patron that does not exist"""
    mocker.patch("patrons.patron_controller.get_patron_from_db", return_value=None)
    with pytest.raises(PatronNotFound):
        search_for_patron("prePatron3")


def test_edit_patron(mocker, test_teacher_basemodel, test_edit_patron_basemodel):
    """Test editing a patron"""
    mocker.patch(
        "patrons.patron_controller.search_for_patron",
        return_value=test_teacher_basemodel,
    )
    edit_patron = mocker.patch(
        "patrons.patron_controller.update_patron_info_in_db", return_value=None
    )
    update_patron(EXAMPLE_OBJECT_ID, test_edit_patron_basemodel)
    edit_patron.assert_called_once_with(
        test_teacher_basemodel,
        **test_edit_patron_basemodel.model_dump(exclude_none=True),
    )


def test_get_patron_from_db(save_patron_then_delete, test_student_document):
    get_patron = get_patron_from_db(test_student_document.id)
    assert get_patron.name == test_student_document.name
    # Have to delete patrons for other tests because data persists between tests


def test_get_all_patrons_from_db(
    add_multiple_patrons_then_delete, test_student_document, test_teacher_document
):
    all_patrons = get_all_patrons_from_db(2, 0)
    assert [patron.id for patron in all_patrons] == [
        test_student_document.id,
        test_teacher_document.id,
    ]


def test_update_patron_in_db(mocker, save_patron_then_delete, test_student_document):
    update_patron_info_in_db(test_student_document, "name", "updated")
    assert test_student_document.name == "updated"


def test_get_patron_route(mocker, client, test_student_return_basemodel):
    mocker.patch(
        "patrons.patron_routes.get_patron", return_value=test_student_return_basemodel
    )
    model_json = test_student_return_basemodel.model_dump()
    test_response = client.get(f"/patrons/{EXAMPLE_OBJECT_ID}")
    assert test_response.status_code == SUCCESSFUL_HTTP_CODE
    assert test_response.json()["name"] == model_json["name"]


def test_get_all_patrons_route(mocker, client, test_student_return_basemodel):
    mocker.patch(
        "patrons.patron_routes.get_all_patrons",
        return_value={"items": test_student_return_basemodel.model_dump()},
    )
    test_response = client.get("/patrons")
    assert test_response.status_code == SUCCESSFUL_HTTP_CODE

    assert test_response.json()["items"]["id"] == EXAMPLE_OBJECT_ID


def test_update_patron_route(mocker, client, test_edit_patron_basemodel):
    model_dict = test_edit_patron_basemodel.model_dump(exclude_none=True)
    mock_patch = mocker.patch(
        "patrons.patron_routes.update_patron",
        return_value=None,
    )
    response = client.patch(
        f"/patrons/{EXAMPLE_OBJECT_ID}",
        json=model_dict,
    )
    mock_patch.assert_called_once_with(EXAMPLE_OBJECT_ID, test_edit_patron_basemodel)
    assert response.status_code == SUCCESSFUL_HTTP_CODE


def test_remove_patron_route(mocker, client):
    mock_delete = mocker.patch(
        "patrons.patron_routes.remove_patron",
        return_value=None,
    )
    response = client.delete(f"/patrons/{EXAMPLE_OBJECT_ID}")
    mock_delete.assert_called_once_with("12345")
    assert response.status_code == SUCCESSFUL_HTTP_CODE
