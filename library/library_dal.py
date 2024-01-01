"""General DAL functionality for adding/deleting from DB"""
from beanie import Document


async def remove_from_db(model: Document) -> None:
    """Generic funtion to delete a function from DB

    :param model: document to delete
    :type model: Document
    """
    await model.delete()


async def add_to_db(model: Document) -> str:
    """Generic function to add a document to db

    :param model: document to add
    :type model: Document
    :return: object ID of document
    :rtype: str
    """
    await model.insert()
    return model.id
