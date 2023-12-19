""" Bussiness logic layer for patrons of library"""
from mongoengine import ValidationError

from patrons.patron_model import (
    PatronBase,
    PatronModel,
    TeacherModel,
    StudentModel,
    TeacherBase,
    StudentBase,
)
from patrons.patron_base import PatronTypes
from library.library_dal import add_to_db, remove_from_db
from patrons.patron_dal import (
    get_patron_from_db,
    update_patron_info_in_db,
    get_all_patrons_from_db,
)
from library.library import ProtectedAttribute
import json


class PatronNotFound(Exception):
    """Exception raised if patron not found in library"""


class PatronModelFactory:
    """Patron model factory class"""

    def create_model(self, patron: PatronBase):
        """creates patron document model from basemodel

        Args:
            patron (PatronBase): patron basemodel

        Returns:
            _type_: patron document model
        """
        match patron.category:
            case PatronTypes.TEACHER.name:
                db_model = TeacherModel(**patron.model_dump())
            case PatronTypes.STUDENT.name:
                db_model = StudentModel(**patron.model_dump())
            case default:
                db_model = PatronModel(**patron.model_dump())
        return db_model

    def create_basemodel(self, patron_model: PatronModel):
        """generates patron basemodel from document model

        Args:
            patron_model (PatronModel): patron document model

        Returns:
            _type_: patron basemodel
        """

        match patron_model.category:
            case PatronTypes.TEACHER.name:
                patron_basemodel = TeacherBase(**patron_model.to_mongo().to_dict())
            case PatronTypes.STUDENT.name:
                patron_basemodel = StudentBase(**patron_model.to_mongo().to_dict())
            case default:
                patron_basemodel = PatronBase(**patron_model.to_mongo().to_dict())
        return patron_basemodel


def create_patron(patron: PatronBase) -> str:
    """accepts a patron model and adds it to db

    Args:
        patron (PatronBase): Patron basemodel

    Returns:
        str: patron mongo id
    """
    db_model = PatronModelFactory().create_model(patron=patron)
    patron_id = add_to_db(db_model)
    return str(patron_id)


def search_for_patron(patron_id: str) -> PatronModel:
    """search for patron in DB. raise PatronNotFound if not found

    Args:
        patron_id (str): patron mongo id

    Raises:
        PatronNotFound: raised if no patron with given id is found

    Returns:
        PatronModel: patron document model
    """
    try:
        patron_db_model = get_patron_from_db(patron_id)
    except ValidationError as exc:
        raise PatronNotFound(f"patron with ID: {patron_id} not found in DB") from exc
    if patron_db_model is None:
        raise PatronNotFound(f"patron with ID: {patron_id} not found in DB")
    return patron_db_model


def get_patron(patron_id: str) -> PatronBase:
    """searches for a patron and returns it's basemodel

    Args:
        patron_id (str): Patron ID

    Raises:
        PatronNotFound: if patron with ID is not found

    Returns:
        PatronBase: patron basemodel
    """
    patron_db_model = search_for_patron(patron_id)
    patron_model = PatronModelFactory().create_basemodel(patron_db_model)
    return patron_model


def remove_patron(patron_id: str) -> None:
    """checks if patron exists and deletes it fromn DB

    Args:
        patron_id (str): patron ID
    """
    patron_model = search_for_patron(patron_id)
    remove_from_db(patron_model)


def update_patron(patron_id: str, attribute: str, new_value: str) -> None:
    """Checks if patron exists and updates it's info

    Args:
        patron_id (str): patron id
        attribute (str): attribute to update
        new_value (str): new value of attribute
    """
    if attribute.upper() == "FINES" or attribute.upper() == "FINE_DISCOUNT":
        raise ProtectedAttribute(f"Cannot edit a patron's {attribute}")
    patron_model = search_for_patron(patron_id)

    update_patron_info_in_db(patron_model, attribute, new_value)


def get_all_patrons() -> [PatronBase]:
    """returns an array of the basemodel of all patrons

    Returns:
        [PatronModel]: array of basemodel of all patrons
    """
    model_list = get_all_patrons_from_db()
    response_list = []
    model_factory = PatronModelFactory()
    for patron_model in model_list:
        response_list.append(model_factory.create_basemodel(patron_model=patron_model))
    return response_list
