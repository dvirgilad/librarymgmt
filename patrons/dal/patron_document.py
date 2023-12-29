import json
from mongoengine import DictField, Document, FloatField, IntField, StringField
from bson import son, json_util
from consts import MONGO_OID_PREFIX


class PatronModel(Document):
    """Patron model for DB"""

    name = StringField(required=True)
    category = StringField()
    fines = IntField(0)
    fine_discount = FloatField(0.0)
    patron_attributes = DictField()

    @staticmethod
    def __beautify_id(data: dict) -> None:
        data["id"] = str(data["_id"])
        del data["_id"]

    @staticmethod
    def __beautify_oid(data_dict: dict) -> dict:
        """
        Recieves a dict of mongo data and returns with the oid as a string.
        :param data_dict: dict of mongo object data
        :return: The modified dict with oid as string
        """

        return {
            key: value.get(MONGO_OID_PREFIX)
            if isinstance(value, dict) and value.get(MONGO_OID_PREFIX)
            else value
            for key, value in data_dict.items()
        }

    def to_json(self, *args, **kwargs):
        raw_data = self.to_mongo()
        self.__beautify_id(raw_data)
        return json_util.dumps(son.SON(raw_data), *args, **kwargs)

    def to_dict(self, *args, **kwargs) -> dict:
        """Convert this document to a python dict

        Returns:
            dict: dict containing values of document
        """
        object_data = json.loads(self.to_json())
        return self.__beautify_oid(object_data)
