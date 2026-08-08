'''To design a **Library Management System** in Python while following the **Singleton** and **Observer** design patterns,
we will need the following entities:

1. **Library (Singleton)**: The library itself will be a singleton, meaning that only one instance of the library can exist
at any time.
2. **User**: Represents a user of the library who can borrow and return books.
3. **Librarian**: The librarian who manages the books in the library and oversees check-in and check-out operations.
4. **BookBorrowed (Observer)**: Represents the action of borrowing books. Users are observers and will be notified when the
status of books changes (whether the book is checked out or returned).
5. **Books**: Represents the collection of books available in the library.

Design Steps:
1. **Singleton Pattern**: The library class will follow the Singleton pattern to ensure only one instance exists.
2. **Observer Pattern**: Users will be observers of book availability. If a book is borrowed or returned, users waiting for
that book will be notified.
'''

# Observer Pattern for book borrowing and return
class Observer:
    def update(self, book_name, message):
        raise NotImplementedError("Subclass must implement abstract method")

class User(Observer):
    def __init__(self, user_name):
        self.user_name = user_name

    def update(self, book_name, message):
        print(f"User {self.user_name} notified: {book_name} {message}")

# Singleton Library
class Library:
    _instance = None

    @staticmethod
    def get_instance():
        if Library._instance is None:
            Library._instance = Library()
        return Library._instance

    def __init__(self):
        if Library._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.books = {}  # Dictionary to store book names and their quantities
            self.borrowed_books = {}  # Dictionary to track borrowed books
            self._observers = []  # List of users waiting for books

    # Librarian adds books to the library
    def add_book(self, book_name, quantity=1):
        if book_name in self.books:
            self.books[book_name] += quantity
        else:
            self.books[book_name] = quantity
        print(f"{quantity} copies of {book_name} added to the library")

    # Attach users who want to observe changes in book status
    def attach(self, user):
        self._observers.append(user)

    # Detach user from observing
    def detach(self, user):
        self._observers.remove(user)

    # Notify users when the book's status changes (checked out or returned)
    def notify(self, book_name, message):
        for observer in self._observers:
            observer.update(book_name, message)

    # Librarian can check if a book is available
    def is_book_available(self, book_name):
        return self.books.get(book_name, 0) > 0

    # Check out a book from the library
    def checkout_book(self, user, book_name):
        if self.is_book_available(book_name):
            self.books[book_name] -= 1
            self.borrowed_books[user.user_name] = book_name
            print(f"User {user.user_name} checked out {book_name}")
            self.notify(book_name, "has been checked out")
        else:
            print(f"Sorry, {book_name} is not available")

    # Return a book to the library
    def return_book(self, user):
        if user.user_name in self.borrowed_books:
            book_name = self.borrowed_books.pop(user.user_name)
            self.books[book_name] += 1
            print(f"User {user.user_name} returned {book_name}")
            self.notify(book_name, "is now available")
        else:
            print(f"User {user.user_name} has no borrowed books")

# Librarian (uses Singleton Library)
class Librarian:
    def __init__(self, name):
        self.name = name
        self.library = Library.get_instance()

    def add_book_to_library(self, book_name, quantity=1):
        self.library.add_book(book_name, quantity)

    def check_out_book(self, user, book_name):
        self.library.checkout_book(user, book_name)

    def accept_returned_book(self, user):
        self.library.return_book(user)


# Example usage
if __name__ == "__main__":
    # Initialize singleton library and librarian
    librarian = Librarian("John")

    # Add books to the library
    librarian.add_book_to_library("The Great Gatsby", 3)
    librarian.add_book_to_library("1984", 2)

    # Create users
    user1 = User("Alice")
    user2 = User("Bob")

    # Attach users as observers to the library
    library = Library.get_instance()
    library.attach(user1)
    library.attach(user2)

    # Check out and return books
    librarian.check_out_book(user1, "The Great Gatsby")
    librarian.check_out_book(user2, "1984")
    
    # Return a book
    librarian.accept_returned_book(user1)

    # Check out the returned book again
    librarian.check_out_book(user2, "The Great Gatsby")

'''
Explanation:
1. **Library (Singleton)**:
   - The library class is implemented using the Singleton pattern to ensure only one instance of the library is created.
   - It holds information about available and borrowed books, and a list of users who observe changes in book availability.

2. **User (Observer)**:
   - Users can borrow and return books. They are observers and get notified when the availability of the books changes.

3. **Librarian**:
   - The librarian acts as an interface for adding books to the library, checking books out, and returning them.

4. **BookBorrowed (Observer Pattern)**:
   - When a book is borrowed or returned, users observing that book will be notified about its status.


Summary:
- **Singleton Pattern** ensures only one library exists.
- **Observer Pattern** allows users to be notified when a book is borrowed or returned.
- The system handles the addition of books, check-in, and check-out operations via a librarian entity.
'''