"""Data access layer for library items"""
from library_item.library_item_model import LibraryItemModel


def get_library_item_from_db(library_item_id: str) -> LibraryItemModel:
    """accepts library item id and returns LibraryModel"""
    library_item_obj = LibraryItemModel.objects(id=library_item_id).get()
    return library_item_obj


def get_all_library_items_from_db(limit: int, skip: int) -> [LibraryItemModel]:
    """Gets all library items from DB

    Args:
        limit(int): how many results to return
        skip(int): how many results to skip

    Returns:
        [LibraryItemModel]: array of library items to return
    """
    return LibraryItemModel.objects[skip:limit]


def update_libray_items_info_in_db(
    library_item_model: LibraryItemModel,
    attribute: str = None,
    new_value: str = None,
    **kwargs,
) -> None:
    """changes the given attribute of the given item in DB

    Args:
        library_item_model (LibraryItemModel): library_item to update
        attribute (str): attribute to update
        new_value (str): new value of the attribute
    """
    if not attribute or not new_value:
        for attrib, value in kwargs.items():
            library_item_model.modify(**{f"set__{attrib.lower()}": value})
    else:
        library_item_model.modify(**{f"set__{attribute.lower()}": new_value})
    library_item_model.save()


def search_library_items_in_db(
    query_string: str, limit: int, skip: int
) -> [LibraryItemModel]:
    """search library items for a specific string

    Args:
        query_string (str): string to match

    Returns:
        [LibraryItemModel]: list of library items that match query
    """
    print(1)
    return LibraryItemModel.objects.search_text(query_string)[skip:limit]