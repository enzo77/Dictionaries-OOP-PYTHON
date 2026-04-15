class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

class User:
    def __init__(self, name, dni, age):
        self.name = name
        self.dni = dni
        self.age = age

class Library:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.books = []
        self.loans = {}

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def lend_book(self, title, user):
        book = self.find_book(title)
        if book:
            self.loans[user.dni] = book

    def return_book(self, title, user):
        if user.dni in self.loans:
            del self.loans[user.dni]
            
lib = Library("Central Library", "Barcelona")

b1 = Book("9780441172719", "Dune", "Frank Herbert")
b2 = Book("9780451524935", "1984", "George Orwell")

u1 = User("Alice", "12345678A", 30)
u2 = User("Bob", "87654321B", 25)

lib.add_book(b1)
lib.add_book(b2)

lib.add_book(Book("9780261103573", "The Hobbit", "J.R.R. Tolkien"))

lib.lend_book("Dune", u1)
lib.return_book("Dune", u1)

book = lib.find_book("1984")

print(f"book" , {lib})