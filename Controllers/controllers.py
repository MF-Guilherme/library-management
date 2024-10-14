from Models.models import Book, User
from Exceptions.exceptions import DuplicateError, LenOfPhoneError, EmailFormatError
from db_connection import get_connection
from datetime import datetime
import re, psycopg2


class BookController():
    def __init__(self) -> None:
        self.conn = get_connection()
        if self.conn is not None:
            self.cursor = self.conn.cursor()
        else:
            raise Exception("Failed to establish database connection")

    def validate_empty_fields(self, title, author, year, genre, code):
        # validate if any field is empty
        if not title or not author or not year or not genre or not code:
            raise ValueError('Not registered! Please, enter all fields.')

    def validate_numeric_fields(self, year, code):
        # validate if year and code are numerics
        if not year.isnumeric() and not code.isnumeric():
            raise ValueError(
                'Not registered! The Publication Year and ISBN Code must contain numbers')
        if not year.isnumeric():
            raise ValueError(
                'Not registered! Publication Year must contain numbers')
        if not code.isnumeric():
            raise ValueError('Not registered! ISBN Code must contain numbers')

    def validate_non_numeric_fields(self, title, author, genre):
        # validate if title, author and genre aren't just numbers
        if title.isnumeric():
            raise ValueError(
                "Not registered! The Title field can't contain just numbers")
        if author.isnumeric():
            raise ValueError(
                "Not registered! The Author field can't contain just numbers")
        if genre.isnumeric():
            raise ValueError(
                "Not registered! The Literary genre field can't contain just numbers")

    def validate_year_publication(self, year):
        # validate if the year field is less than the current year
        current_year = datetime.now().year
        if int(year) > current_year:
            raise ValueError(
                "Not registered! Publication year must be less than or equal to the current year")
        if len(str(year)) < 3:
            raise ValueError(
                "Not registered! Publication year must contain at least 3 digits.")

    def validate_book_fields(self, title, author, year, genre, code):
        year = str(year)
        self.validate_empty_fields(title, author, year, genre, code)
        self.validate_numeric_fields(year, code)
        self.validate_non_numeric_fields(title, author, genre)
        self.validate_year_publication(year)

    def add_book(self, title, author, year, genre, code):
        if self.search_by_book_code(code):
            raise DuplicateError(code)

        self.validate_book_fields(title, author, year, genre, code)
        query = "INSERT INTO books (title, author, year, genre, isbn_code) VALUES (%s, %s, %s, %s, %s);"
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (title, author, year, genre, code,))
        return "Success! Book registered!"
   
    def list_all_books(self):
        query = "SELECT * FROM books"
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        if result:
            return result
        else:
            return None

    def search_by_book_code(self, code):
        query = "SELECT * FROM books WHERE isbn_code = %s"
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (code, ))
                result = cursor.fetchone()
        if result:
            return result
        else:
            return None
          
    def update_book(self, code, title=None, author=None, year=None, genre=None):
        query = ("""
                 UPDATE books SET (title, author, year, genre) = (%s, %s, %s, %s)
                 WHERE isbn_code = %s;
                 """)
        book = self.search_by_book_code(code)
        if book is None:
            return None
        else:
            self.validate_book_fields(title, author, year, genre, code)
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (title, author, year, genre, code, ))        
            return True

    def delete_book(self, code):
        query = "DELETE FROM books WHERE isbn_code = %s"
        book = self.search_by_book_code(code)
        if book:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (code, ))
            return True
        return False


class UserController():
    def __init__(self) -> None:    
        self.conn = get_connection()
        if self.conn is not None:
            self.cursor = self.conn.cursor()
        else:
            raise Exception("Failed to establish database connection")

    def validate_empty_fields(self, name, email, phone, user_code):
        if not name or not email or not phone or not user_code:
            raise ValueError('Not registered! Please, enter all fields')

    def validate_non_numeric_fields(self, name, email):
        if name.isnumeric():
            raise ValueError(
                "Not registered! Name field can't contain just numbers")
        if email.isnumeric():
            raise ValueError(
                "Not registered! Email field can't contain just numbers")

    def validate_numeric_fields(self, phone, user_code):
        if not phone.isnumeric():
            raise ValueError(
                "Not registered! Phone field must contain just numbers")
        if type(user_code) is not int :
            raise TypeError(
                "Not registered! User code field must contain just numbers")

    def validate_len_phone(self, phone):
        if not len(phone) >= 10 or not len(phone) <= 11:
            raise LenOfPhoneError()

    def validate_email_format(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, email):
            raise EmailFormatError(email)

    def validate_user_fields(self, name, email, phone, user_code):
        self.validate_empty_fields(name, email, phone, user_code)
        self.validate_non_numeric_fields(name, email)
        self.validate_numeric_fields(phone, user_code)
        self.validate_len_phone(phone)
        self.validate_email_format(email)

    def register_user(self, name, email, phone, user_code):
        if self.find_by_user_code(user_code):
            raise DuplicateError(user_code, entity="User")
        with self.conn:
            with self.conn.cursor() as cursor:
                self.validate_user_fields(name, email, phone, user_code)
                query = "INSERT INTO users (name, email, phone, user_code) VALUES (%s, %s, %s, %s);"
                cursor.execute(query, (name, email, phone, user_code, ))
        return "Success! User registered."

    def list_users(self):
        return self.db

    def find_by_user_code(self, user_code):
        query = "SELECT * FROM users WHERE user_code = %s"
        with self.conn:
            with self.conn.cursor() as cursor:
                user = cursor.execute(query, user_code).fetchone()
        if user:
            return user
        else:
            return None

    def delete_user(self, user_code):
        user = self.find_by_user_code(user_code)
        if user:
            self.db.remove(user)
            return True
        return False

    def update_user(self, user_code, name=None, email=None, phone=None):
        user = self.find_by_user_code(user_code)
        if user is None:
            return None
        else:
            self.validate_user_fields(name, email, phone, user_code)
            if name:
                user.name = name
            if email:
                user.email = email
            if phone:
                user.phone = phone
            return True
