"""MongoEngine model for library"""
from mongoengine import Document, StringField


class LibraryModel(Document):
    """Library model for DB"""

    name = StringField(required=True)
