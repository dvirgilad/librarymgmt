"""General DAL functionality for adding/deleting from DB"""
from mongoengine import Document


def remove_from_db(model: Document) -> None:
    """Generic funtion to delete a function from DB

    :param model: document to delete
    :type model: Document
    """
    model.delete()


def add_to_db(model: Document) -> str:
    """Generic function to add a document to db

    :param model: document to add
    :type model: Document
    :return: object ID of document
    :rtype: str
    """
    model.save()
    return model.pk
