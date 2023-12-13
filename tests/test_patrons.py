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
from patrons.patron_dal import (
    get_all_patrons_from_db,
    get_patron_from_db,
    update_patron_info_in_db,
)
from patrons.patron_model import PatronModel


def test_add_teacher(mocker, test_teacher_basemodel):
    mocker.patch.object(
        PatronModelFactory, "create_model", return_value=test_teacher_basemodel
    )
    mocker.patch("patrons.patron_controller.add_to_db", return_value="12345")
    test_id = create_patron(test_teacher_basemodel)
    assert test_id == "12345"


def test_add_student(mocker, test_student_basemodel):
    mocker.patch.object(
        PatronModelFactory, "create_model", return_value=test_student_basemodel
    )
    mocker.patch("patrons.patron_controller.add_to_db", return_value="12345")
    test_id = create_patron(test_student_basemodel)
    assert test_id == "12345"


def test_remove_patron(mocker):
    """Test removing a patron from the library"""
    mocker.patch(
        "patrons.patron_controller.search_for_patron", return_value={"name": "12345"}
    )
    patch_remove = mocker.patch(
        "patrons.patron_controller.remove_from_db", return_value=None
    )
    remove_patron("12345")
    patch_remove.assert_called_once_with({"name": "12345"})


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


def test_edit_patron(mocker, test_teacher_basemodel):
    """Test editing a patron"""
    mocker.patch(
        "patrons.patron_controller.search_for_patron",
        return_value=test_teacher_basemodel,
    )
    edit_patron = mocker.patch(
        "patrons.patron_controller.update_patron_info_in_db", return_value=None
    )
    update_patron("12345", "test_attribute", "test_value")
    edit_patron.assert_called_once_with(
        test_teacher_basemodel, "test_attribute", "test_value"
    )


def test_get_patron_from_db(mocker):
    test_patron_model = PatronModel(name="test")
    test_patron_model.save()
    get_patron = get_patron_from_db(test_patron_model.id)
    assert get_patron.name == "test"
    ## Have to delete patrons for other tests because data persists between tests
    test_patron_model.delete()


def test_get_all_patrons_from_db(mocker):
    test_patron_model = PatronModel(name="test")
    test_patron_model.save()
    test_patron_model2 = PatronModel(name="test2")
    test_patron_model2.save()
    all_patrons = get_all_patrons_from_db()

    assert [patron.id for patron in all_patrons] == [
        test_patron_model.id,
        test_patron_model2.id,
    ]

    test_patron_model.delete()
    test_patron_model2.delete()


def test_update_patron_in_db(mocker):
    test_patron_model = PatronModel(name="test")
    test_patron_model.save()
    update_patron_info_in_db(test_patron_model, "name", "updated")
    assert test_patron_model.name == "updated"
    test_patron_model.delete()
