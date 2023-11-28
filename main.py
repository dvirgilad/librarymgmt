import time
from library import Library
from patrons import Student, Teacher
from items import Book, Disk


def run_library():

    L = Library("DPL", [], [])
    teach1 = Teacher("steve", "math")
    teach2 = Teacher("Jack", "CS")
    stu1 = Student("bob", "Econ")
    stu2 = Student("Alice", "Art")
    stu3 = Student("Howard", "bussiness")
    L.add_patrons(teach1)

    L.add_patrons(patron_list=[teach2, stu1, stu2, stu3])
    print("Members:")
    L.show_members()
    print("\n\n\n")
    time.sleep(3)
    b1 = Book("Pride & Prejudice", "Jane Austin", "drama")
    b2 = Book("Dune", "Frank Herbert", "Sci-Fi")
    b3 = Book("The Odyssey", "Homer", "greek")
    b4 = Book("The Illiad", "Homer", "greek")
    b5 = Book("C Programming Language", "Brian W. Kernighan", "Cool")

    c1 = Disk("Blonde", "Frank Ocean", "R&B")
    c2 = Disk("Meteora", "Linkin Park", "Punk")
    c3 = Disk("AM", "Arctic Monekys", "Rock")
    c4 = Disk("Swimming", "Mac Miller", "Rap")

    L.add_Item(item_list=[b1, b2, b3, b4, b5, c1, c2, c3, c4])
    time.sleep(2)
    print("Catalog:")
    L.show_catalog()
    print("\n\n\n")
    time.sleep(3)
    print("Searching the library for Homer... results:")
    L.search_library("homer")

    print("\n\n\n")
    time.sleep(2)
    b3.borrow(stu1)

    b3.borrow(stu2)
    time.sleep(2)
    b3.unborrow()
    print("\n\n\n")
    stu1.get_fines()


if __name__ == '__main__':
    run_library()
