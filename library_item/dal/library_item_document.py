import json
from bson import son, json_util
from mongoengine import (
    StringField,
    IntField,
    BooleanField,
    DateTimeField,
    DynamicDocument,
    DictField,
)
from consts import MONGO_OID_PREFIX, MONGO_DATE_PREFIX


class LibraryItemModel(DynamicDocument):
    """Library item model for DB"""

    name = StringField(required=True)
    genre = StringField()
    fine = IntField(0)
    category = StringField()
    borrowing_period = IntField(0)
    borrowed_status = BooleanField(default=False)
    # borrower = ReferenceField(PatronModel)
    borrowed_at = DateTimeField(default=None)
    library_item_attributes = DictField()
    meta = {
        "indexes": [
            {
                "name": "text_index",
                "fields": ["$name", "$genre"],
                "default_language": "none",
                "weights": {"name": 5, "genre": 4},
            }
        ],
    }

    @staticmethod
    def __beautify_id(data: dict) -> None:
        data["id"] = str(data["_id"])
        del data["_id"]

    @staticmethod
    def __beautify_oid(data_dict: dict) -> dict:
        """
        Recieves a dict of mongodata and returns with the oid and date as a string.
        :param data_dict: dict of mongo object data
        :return: The modified dict with oid and date as string
        """
        response_dict = {}
        for key, value in data_dict.items():
            if isinstance(value, dict) and value.get(MONGO_OID_PREFIX):
                response_dict[key] = value.get(MONGO_OID_PREFIX)
            elif isinstance(value, dict) and value.get(MONGO_DATE_PREFIX):
                response_dict[key] = value.get(MONGO_DATE_PREFIX)
            else:
                response_dict[key] = value
        return response_dict

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
