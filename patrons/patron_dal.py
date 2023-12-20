"""Data access layer for patrons"""
from patrons.patron_model import PatronModel


def get_patron_from_db(patron_id: str) -> PatronModel:
    """accepts patron id and returns PatronModel"""
    patron_obj = PatronModel.objects(id=patron_id).first()
    return patron_obj


def get_all_patrons_from_db(limit: int, skip: int) -> [PatronModel]:
    """Returns all patrons from DB"""
    return PatronModel.objects[skip:limit]


def update_patron_info_in_db(
    patron_model: PatronModel, attribute: str, new_value: str | int
) -> None:
    """update the attributes of a patron in the db

    Args:
        patron_model (PatronModel): patron documnet model
        attribute (str | int): attribute to change the value of
        new_value (str): new value of attribute
    """
    patron_model.modify(**{f"set__{attribute}": new_value})
    patron_model.save()
