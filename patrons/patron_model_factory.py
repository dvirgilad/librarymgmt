"""Factory to create patron basemodel or document"""
from .dal.patron_model import PatronCreate, PatronReturn
from .dal.patron_document import PatronModel


class PatronModelFactory:
    """Patron model factory class"""

    @staticmethod
    def create_model(patron: PatronCreate) -> PatronModel:
        """Create a mongo document from a patron basemodel

        :param patron: patron basemodel
        :type patron: PatronCreate
        :return: patron document model
        :rtype: PatronModel
        """

        db_model = PatronModel(**patron.model_dump())
        return db_model

    @staticmethod
    def create_basemodel(patron_model: PatronModel) -> PatronReturn:
        """Create a basemodel from a patron document

        :param patron_model: patron mongo document
        :type patron_model: PatronModel
        :return: patron Basemodel
        :rtype: PatronReturn
        """

        patron_basemodel = PatronReturn(**patron_model.to_dict())
        return patron_basemodel
