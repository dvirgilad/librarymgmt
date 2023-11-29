from library_item.library_item_base import LibraryItem
from patrons.patron_base import Patron


class Library:
    def __init__(self, name, patrons: [Patron], library_items={}):
        name, self.library_items, self.patrons = name, library_items, patrons

    def show_members(self):
        for member in self.patrons:
            print(f"{member.name}:\t{member.category} ")

    def show_catalog(self):
        for key, library_item in self.library_items.items():
            print(
                f"{library_item.name}\t\t\t {library_item.type}\t\t\t {library_item.serial}"
            )

    def add_item(self, library_item: LibraryItem):
        self.library_items[id(library_item)] = library_item
        print(f"added {library_item.name}")
        return True

    def add_items(self, library_item_list: [LibraryItem]):
        for library_item in library_item_list:
            self.add_item(library_item)

    def remove_item(self, item_to_remove: LibraryItem):
        try:
            del self.library_items[id(item_to_remove)]
            print(f"{item_to_remove} removed")
            return True
        except KeyError:
            print("book not found")
            return False

    def add_patrons(self, member: Patron = None, patron_list: [Patron] = []):
        if member:
            self.patrons.append(member)
            print(f"{member.name} has joined the Library")
        else:
            for patron in patron_list:
                self.patrons.append(patron)
                print(f"{patron.name} has joined the Library")

    def search_library(self, query: str):
        result = []
        for key, library_item in self.library_items.items():
            if library_item.match_string(query):
                result.append(library_item)
                print(library_item.name)
        return result
