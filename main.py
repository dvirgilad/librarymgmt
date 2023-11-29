import time
from library.library import Library
from patrons.student import Student
from patrons.teacher import Teacher
from library_item.book import Book
from library_item.disk import Disk


def run_library():
    L = Library("DPL", [])
    # teach1 = Teacher("steve", "math")
    # teach2 = Teacher("Jack", "CS")
    # stu1 = Student("bob", "Econ")
    # stu2 = Student("Alice", "Art")
    # stu3 = Student("Howard", "bussiness")
    # L.add_patrons(teach1)

    # L.add_patrons(patron_list=[teach2, stu1, stu2, stu3])
    # print("Members:")
    # L.show_members()
    # print("\n\n\n")
    # time.sleep(3)
    # b1 = Book("Pride & Prejudice", "Jane Austin", "drama", 30, 30)
    # b2 = Book("Dune", "Frank Herbert", "Sci-Fi", 100, 20)
    # b3 = Book("The Odyssey", "Homer", "greek", 500, 10)
    # b4 = Book("The Illiad", "Homer", "greek", 10, 20)
    # b5 = Book("C Programming Language", "Brian W. Kernighan", "Cool", 5, 100)

    c1 = Disk("Blonde", "Frank Ocean", "R&B", 30, 30)
    # c2 = Disk("Meteora", "Linkin Park", "Punk", 100, 20)
    # c3 = Disk("AM", "Arctic Monekys", "Rock", 10, 20)
    # c4 = Disk("Swimming", "Mac Miller", "Rap", 5, 100)

    # L.add_items(library_item_list=[b1, b2, b3, b4, b5, c1, c2, c3, c4])
    # time.sleep(2)
    # print("Catalog:")
    # L.show_catalog()
    # print("\n\n\n")
    # time.sleep(3)
    # print("Searching the library for Homer... results:")
    # L.search_library("homer")

    # print("\n\n\n")
    # time.sleep(2)
    # b3.borrow(stu1)

    # b3.borrow(stu2)
    # time.sleep(2)
    # b3.unborrow()
    # print("\n\n\n")
    # stu1.get_fines()
    c1.update_item("name", "123")


if __name__ == "__main__":
    run_library()
