"""Data access layer for patrons"""
from patrons.dal.patron_model import PatronModel
from beanie.operators import Set


async def get_patron_from_db(patron_id: str) -> PatronModel:
    """Gets a patron from db by id

    :param patron_id: ID of patron
    :type patron_id: str
    :return: Patron document
    :rtype: PatronModel
    """
    patron_obj = await PatronModel.get(document_id=patron_id)
    return patron_obj


async def get_all_patrons_from_db(limit: int, skip: int) -> [PatronModel]:
    """Returns patrons from db based on limit and skip

    :param limit: how many documents to return
    :type limit: int
    :param skip: how many patrons to skip
    :type skip: int
    :return: array of patrons
    :rtype: [PatronModel]
    """
    return await PatronModel.find_all(skip=skip, limit=limit).to_list()


async def update_patron_info_in_db(
    patron_model: PatronModel,
    attribute: str = None,
    new_value: str | int = None,
    **kwargs,
) -> None:
    """Change info of patron in db

    :param patron_model: model of patron to edit
    :type patron_model: PatronModel
    async :param attribute: attribute to edit, defaults to None
    :type attribute: str, optional
    async :param new_value: new value of attribute, defaults to None
    :type new_value: str | int, optional
    """
    if kwargs:
        await patron_model.update(Set(kwargs))
    if attribute and new_value:
        await patron_model.update(Set({attribute: new_value}))
    await patron_model.save()
