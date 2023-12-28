"""Data access layer for patrons"""
from patrons.dal.patron_document import PatronModel


def get_patron_from_db(patron_id: str) -> PatronModel:
    """Gets a patron from db by id

    :param patron_id: ID of patron
    :type patron_id: str
    :return: Patron documnet
    :rtype: PatronModel
    """
    patron_obj = PatronModel.objects(id=patron_id).first()
    return patron_obj


def get_all_patrons_from_db(limit: int, skip: int) -> [PatronModel]:
    """Returns patrons from db based on limit and skip

    :param limit: how many documents to return
    :type limit: int
    :param skip: how many patrons to skip
    :type skip: int
    :return: array of patrons
    :rtype: [PatronModel]
    """
    return PatronModel.objects[skip:limit]


def update_patron_info_in_db(
    patron_model: PatronModel,
    attribute: str = None,
    new_value: str | int = None,
    **kwargs,
) -> None:
    """Change info of patron in db

    :param patron_model: model of patron to edit
    :type patron_model: PatronModel
    :param attribute: attribute to edit, defaults to None
    :type attribute: str, optional
    :param new_value: new value of attribute, defaults to None
    :type new_value: str | int, optional
    """
    for (
        attrib,
        value,
    ) in kwargs:
        for attrib, value in kwargs.items():
            PatronModel.modify(**{f"set__{attrib.lower()}": value})
    if attribute and new_value:
        patron_model.modify(**{f"set__{attribute}": new_value})
    patron_model.save()
