"""General DAL functionality for adding/deleting from DB"""
from mongoengine import Document


def remove_from_db(model: Document) -> None:
    """Accepts Document and removes it from DB"""
    model.delete()


def add_to_db(model: Document) -> str:
    """Accepts Document and adds it from DB, returns its ID"""
    model.save()
    return model.pk
