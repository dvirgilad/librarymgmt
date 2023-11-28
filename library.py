from items import Item
from patrons import Patron


class Library:
    def __init__(self, name, items: [Item], patrons: [Patron]):
        name, self.items, self.patrons = name, items, patrons

    def show_members(self):
        for member in self.patrons:
            print("{:<20} {:>}".format(member.name, member.category))

    def show_catalog(self):
        for item in self.items:
            print("{:<30} {:^} {:=}".format(item.name, item.type, item.serial))

    def add_Item(self, item: Item = None, item_list: [Item] = []):
        if item:
            self.items.append(item)
            print(f"added {item.name}")
        else:
            for b in item_list:
                self.items.append(b)
                print(f"added {b.name}")

    def remove_items(self, serial: int):

        item_to_remove = next((item for item in self.items if item.serial == serial))
        if item_to_remove:
            self.items.remove(item_to_remove)
            print(f"{item_to_remove} removed")
        else:
            print("book not found")

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
        for item in self.items:
            if (
                item.match_string(query)
            ):
                result.append(item)
                print(item.name)
        return result
