""" Bussiness logic layer for patrons of library"""
from mongoengine import ValidationError
from patrons.dal.patron_document import PatronModel
from patrons.patron_exceptions import PatronNotFound
from patrons.patron_model_factory import PatronModelFactory
from patrons.dal.patron_model import PatronReturn, PatronCreate, PatronEdit
from patrons.dal.patron_dal import (
    get_patron_from_db,
    update_patron_info_in_db,
    get_all_patrons_from_db,
)

from library.library_dal import add_to_db, remove_from_db
from library.library_exceptions import InvalidID, AppException


def create_patron(patron: PatronCreate) -> str:
    """Convert a patron to document and add it to db

    :param patron: Patron basemodel
    :type patron: PatronCreate
    :return: patron ID
    :rtype: str
    """
    try:
        db_model = PatronModelFactory.create_model(patron=patron)
        patron_id = add_to_db(db_model)
        return str(patron_id)
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def search_for_patron(patron_id: str) -> PatronModel:
    """Search for patron by ID and return it's document model

    :param patron_id: ID of patron to search for
    :type patron_id: str
    :raises InvalidID: if patron_id is invalid
    :raises PatronNotFound: If no patron with given ID is found
    :return: Document model of patron
    :rtype: PatronModel
    """
    try:
        patron_db_model = get_patron_from_db(patron_id)
    except ValidationError as exc:
        raise InvalidID(object_id=patron_id) from exc
    if patron_db_model is None:
        raise PatronNotFound(patron_id=patron_id)
    return patron_db_model


def get_patron(patron_id: str) -> PatronReturn:
    """Searches for patron and converts it to basemodel

    :param patron_id: ID of patron to search for
    :type patron_id: str
    :return: Patron basemodel
    :rtype: PatronReturn
    """
    patron_db_model = search_for_patron(patron_id)
    try:
        patron_model = PatronModelFactory.create_basemodel(patron_db_model)
        return patron_model
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def remove_patron(patron_id: str) -> None:
    """searches for patron and removes it

    :param patron_id: ID of patron to remove
    :type patron_id: str
    """
    patron_model = search_for_patron(patron_id)
    try:
        remove_from_db(patron_model)
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def update_patron(patron_id: str, new_patron_info: PatronEdit) -> None:
    """search for patron and update it if it exists

    :param patron_id: id of patron to edit
    :type patron_id: str
    :param new_patron_info: info in patron to edit
    :type new_patron_info: PatronEdit
    :raises AppException: Generic exception
    """
    patron_model = search_for_patron(patron_id)
    try:
        update_patron_info_in_db(
            patron_model, **new_patron_info.model_dump(exclude_none=True)
        )

    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def get_all_patrons(limit: int, skip: int) -> [PatronReturn]:
    """Returns requested amount of patrons

    :param limit: last patron #
    :type limit: int
    :param skip: # of patrons to skip
    :type skip: int
    :return: Array of patron
    :rtype: [PatronReturn]
    """
    try:
        model_list = get_all_patrons_from_db(limit, skip)
        return {
            "items": [
                PatronModelFactory.create_basemodel(patron_model)
                for patron_model in model_list
            ],
            "limit": limit,
            "skip": skip,
        }

    except Exception as exc:
        raise AppException(500, str(exc)) from exc
