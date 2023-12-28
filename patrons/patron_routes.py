"""patron fastapi routes"""
from typing import Annotated
from fastapi import APIRouter, Query
from patrons.dal.patron_model import PatronReturn, PatronCreate, PatronEdit
from patrons.patron_controller import (
    create_patron,
    get_all_patrons,
    get_patron,
    remove_patron,
    update_patron,
)
from consts import PaginationDefaults

PATRON_ROUTER = APIRouter()


@PATRON_ROUTER.get("/{patron_id}")
def get_patron_route(patron_id: str) -> PatronReturn:
    """Route to get a patron by ID

    :param patron_id: ID of patron to return
    :type patron_id: str
    :rtype: Patron
    """
    return get_patron(patron_id)


@PATRON_ROUTER.get("/")
def get_all_patrons_route(
    limit: Annotated[
        int, Query(description="Number of patrons to return", ge=1)
    ] = PaginationDefaults.limit,
    skip: Annotated[
        int, Query(description="Number of patrons to skip", ge=0)
    ] = PaginationDefaults.skip,
) -> dict:
    """Route to get all patrons

    :return: Requested items
    :rtype: dict
    """

    return get_all_patrons(limit, skip)


@PATRON_ROUTER.post("/", response_model=str)
def post_patron_route(patron: PatronCreate) -> str:
    """Route to create a patron

    :param patron: patron model
    :type patron: PatronCreate
    :return: ID of created patron
    :rtype: str
    """
    return create_patron(patron)


@PATRON_ROUTER.delete("/{patron_id}")
def delete_patron_route(patron_id: str) -> None:
    """Route to delete a patron by ID

    :param patron_id: ID of patron to delete
    :type patron_id: str
    :raises HTTPException: _description_
    """
    remove_patron(patron_id)


@PATRON_ROUTER.patch("/{patron_id}")
def update_patron_route(patron_id: str, updated_patron: PatronEdit) -> None:
    """Route to edit a patron

    :param patron_id: ID of patron to edit
    :type patron_id: str
    :param updated_patron: patron info to change
    :type updated_patron: PatronEdit
    """
    update_patron(patron_id, updated_patron)
