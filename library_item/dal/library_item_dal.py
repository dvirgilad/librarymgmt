"""Data access layer for library items"""
from library_item.dal.library_item_document import LibraryItemModel


def get_library_item_from_db(library_item_id: str) -> LibraryItemModel:
    """Get item model from db by ID

    :param library_item_id: ID of item to fetch
    :type library_item_id: str
    :return: Library item model
    :rtype: LibraryItemModel
    """
    library_item_obj = LibraryItemModel.objects(id=library_item_id).get()
    return library_item_obj


def get_all_library_items_from_db(limit: int, skip: int) -> [LibraryItemModel]:
    """Returns all library items from db based on skip and limit

    :param limit: number of items to return
    :type limit: int
    :param skip: number of items to skip
    :type skip: int
    :return: array of library item models
    :rtype: [LibraryItemModel]
    """
    return LibraryItemModel.objects[skip:limit]


def update_libray_items_info_in_db(
    library_item_model: LibraryItemModel,
    attribute: str = None,
    new_value: str = None,
    **kwargs,
) -> None:
    """Update the given attribute(s) of an item in DB

    :param library_item_model: Model of item to update
    :type library_item_model: LibraryItemModel
    :param attribute: attribute to edit, defaults to None
    :type attribute: str, optional
    :param new_value: new value of attribute , defaults to None
    :type new_value: str, optional
    """
    if not attribute or not new_value:
        for attrib, value in kwargs.items():
            library_item_model.modify(**{f"set__{attrib.lower()}": value})
    else:
        library_item_model.modify(**{f"set__{attribute.lower()}": new_value})
    print(library_item_model.name)
    library_item_model.save()


def search_library_items_in_db(
    query_string: str, limit: int, skip: int
) -> [LibraryItemModel]:
    """Search text index in DB for a string

    :param query_string: string to search for
    :type query_string: str
    :param limit: amount of results to show
    :type limit: int
    :param skip: amount of reuslts to skip
    :type skip: int
    :return: array of library item models that match the query
    :rtype: [LibraryItemModel]
    """
    return LibraryItemModel.objects.search_text(query_string)[skip:limit]
