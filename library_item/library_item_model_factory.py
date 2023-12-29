from .dal.library_item_document import LibraryItemModel
from .dal.library_item_model import LibraryItemCreate, LibraryItemReturn


class LibraryItemModelFactory:
    """Patron model factory class"""

    @staticmethod
    def create_model(library_item: LibraryItemCreate) -> LibraryItemModel:
        """create a document from a library item basemodel

        :param library_item: _description_
        :type library_item: LibraryItemCreate
        :return: Library item document
        :rtype: LibraryItemModel
        """

        db_model = LibraryItemModel(**library_item.model_dump())
        return db_model

    @staticmethod
    def create_basemodel(library_item_model: LibraryItemModel) -> LibraryItemReturn:
        """create a basemodel from a library item document

        :param library_item_model: library item basemodel
        :type library_item_model: LibraryItemModel
        :return: library item document
        :rtype: LibraryItemReturn
        """
        library_item_basemodel = LibraryItemReturn(**library_item_model.to_dict())
        return library_item_basemodel
