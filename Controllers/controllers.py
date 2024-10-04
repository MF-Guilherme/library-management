from Models.models import Book, User
from datetime import datetime

class BookController():
    def __init__(self) -> None:
        self.db = []

    def validate_empty_fields(self, title, author, year, genre, code):
        # validate if any field is empty
        if not title or not author or not year or not genre or not code:
            raise ValueError('Not registered! Please, enter all fields.')
    
    def validate_numeric_fields(self, year, code):
        # validate if year and code are numerics
        if not year.isnumeric() and not code.isnumeric():
            raise ValueError('Not registered! The Publication Year and ISBN Code must contain numbers')
        if not year.isnumeric():
            raise ValueError('Not registered! Publication Year must contain a number')
        if not code.isnumeric():
            raise ValueError('Not registered! ISBN Code must contain a number')

    def validate_non_numeric_fields(self, title, author, genre):
        # validate if title, author and genre aren't just numbers
        if title.isnumeric():
            raise ValueError("Not registered! The Title field can't contain just numbers")
        if author.isnumeric():
            raise ValueError("Not registered! The Author field can't contain just numbers")
        if genre.isnumeric():
            raise ValueError("Not registered! The Literary genre field can't contain just numbers")
    
    def validate_year_publication(self, year):
        # validate if the year field is less than the current year
        current_year = datetime.now().year
        if int(year) > current_year:
            raise ValueError("Not registered! Publication year must be less than or equal to the current year")
        if len(year) < 3:
            raise ValueError("Not registered! Publication year must contain at least 3 digits.")

    def validate_book_fields(self, title, author, year, genre, code):
        self.validate_empty_fields(title, author, year, genre, code)
        self.validate_numeric_fields(year, code)
        self.validate_non_numeric_fields(title, author, genre)
        self.validate_year_publication(year)        

    def add_book(self, title, author, year, genre, code):
        self.validate_book_fields(title, author, year, genre, code)
        book = Book(title, author, year, genre, code)
        self.db.append(book)

    def list_books(self):
        return self.db
        
    def search_by_book_code(self, code):
        for book in self.db:
            if book.code == code:
                return book
        return None

    def update_book(self, code, title=None, author=None, year=None, genre=None):
        book = self.search_by_book_code(code)
        self.validate_book_fields(title, author, year, genre, code)
        if book:
            if title:
                book.title = title
            if author:
                book.author = author
            if year:
                book.year = year
            if genre:
                book.genre = genre
            return True
        return False
    
    def delete_book(self, code):
        book = self.search_by_book_code(code)
        if book:
            self.db.remove(book)
            return True
        return False


class UserController():
    def __init__(self) -> None:
        self.db = []
    
    def register_user(self, name, email, phone, user_code):
        user = User(name, email, phone, user_code)
        self.db.append(user)
    
    def list_users(self):
        return self.db

    def find_by_user_code(self, user_code):
        for user in self.db:
            if user.user_code == user_code:
                return user
        return None
    
    def delete_user(self, user_code):
        user = self.find_by_user_code(user_code)
        if user:
            self.db.remove(user)
            return True
        return False
    
    def update_user(self, user_code, name=None, email=None, phone=None):
        user = self.find_by_user_code(user_code)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            if phone:
                user.phone = phone
            return True
        return False