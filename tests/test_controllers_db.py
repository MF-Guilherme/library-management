from Models.models import User
from Controllers.controllers import BookController, UserController
from Exceptions.exceptions import DuplicateError, LenOfPhoneError, EmailFormatError
from unittest.mock import patch, MagicMock
from unittest import mock
import pytest, unittest


class TestBookController(unittest.TestCase):

    @patch('Controllers.controllers.get_connection')
    def test_connection_failed(self, mock_get_connection):    
        mock_get_connection.return_value = None

        with pytest.raises(Exception, match="Failed to establish database connection"):
            controller = BookController()

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_add_book_with_valid_data(self, mock_search_by_book_code, mock_get_connection):
        mock_search_by_book_code.return_value = None

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn # Simula "with self.conn"
        mock_conn.cursor.return_value.__enter__.return_value =  mock_cursor # Simula "with self.conn.cursor()"
        mock_get_connection.return_value = mock_conn # Simula "self.conn = get_connection()"

        controller = BookController()

        result = controller.add_book('Title', 'Author', 1990, 'Genre', '123456')

        self.assertEqual(result, "Success! Book registered!")

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO books (title, author, year, genre, isbn_code) VALUES (%s, %s, %s, %s, %s);",
            ('Title', 'Author', 1990, 'Genre', '123456')
            )
        
    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_add_book_raises_duplicate_book_error_when_isbn_code_alredy_registered(self, mock_search_by_book_code):
        mock_search_by_book_code.return_value = ('Some Title', 'Some Author', 1900, 'Some Genre', '789465')

        controller = BookController()

        with pytest.raises(DuplicateError):
            controller.add_book('Some Title', 'Some Author', 1900, 'Some Genre', '789465')

    def test_add_book_raises_ValueError_if_any_field_is_empty(self):
        controller = BookController()

        test_data = [
        ('', 'Some Author', '1234', 'Some Genre', '123456'),  # title is empty
        ('Some Title', '', '1234', 'Some Genre', '123456'),  # author is empty
        ('Some Title', 'Some Author', '', 'Some Genre', '123456'),  # year is empty
        ('Some Title', 'Some Author', '1234', '', '123456'),  # genre is empty
        ('Some Title', 'Some Author', '1234', 'Some Genre', '')  # code is empty
        ]   
        for title, author, year, genre, code in test_data:
            with patch('Controllers.controllers.BookController.search_by_book_code') as mock_search_by_book_code:
                mock_search_by_book_code.return_value = None
                
                with pytest.raises(ValueError):
                    controller.add_book(title, author, year, genre, code)

    def test_add_book_raises_ValueError_if_year_or_book_are_not_numeric(self):
        controller = BookController()

        test_data = [
            ('Some Title', 'Some Author', 'ABCD', 'Some Genre', '12345'),  # year isn't numeric
            ('Some Title', 'Some Author', '1900', 'Some Genre', 'ABCD'),  # code isn't numeric
            ('Some Title', 'Some Author', 'ABCD', 'Some Genre', 'BCDA'), # year and code aren't numeric
        ]

        for title, author, year, genre, code in test_data:
            with patch('Controllers.controllers.BookController.search_by_book_code') as mock_search_by_book_code:
                mock_search_by_book_code.return_value = None

                with pytest.raises(ValueError):
                    controller.add_book(title, author, year, genre, code)

    def test_add_book_raises_ValueError_if_title_author_or_genre_are_not_strings(self):
        controller = BookController()
        
        test_data = [
            ('123456', 'Some Author', '1900', 'Some Genre', '12345'),  # title isn't string
            ('Some Title', '123456', '1900', 'Some Genre', '12345'),  # author isn't string
            ('Some Title', 'Some Author', '1900', '123456', '12345'),  # genre isn't string
        ]

        for title, author, year, genre, code in test_data:
            with patch('Controllers.controllers.BookController.search_by_book_code') as mock_search_by_book_code:
                mock_search_by_book_code.return_value = None
                with pytest.raises(ValueError):
                    controller.add_book(title, author, year, genre, code)

    def test_add_book_raises_ValueError_if_year_doesnt_less_than_or_equal_current_year(self):
        controller = BookController()
        with patch('Controllers.controllers.BookController.search_by_book_code') as mock_search_by_book_code:
            mock_search_by_book_code.return_value = None
            with pytest.raises(ValueError):
                controller.add_book('Some Title', 'Some Author', '2025', 'Some Genre', '4341312')

    def test_add_book_raises_ValueError_if_digits_in_year_field_are_less_than_3(self):
        controller = BookController()
        with patch('Controllers.controllers.BookController.search_by_book_code') as mock_search_by_book_code:
            mock_search_by_book_code.return_value = None
        with pytest.raises(ValueError):
            controller.add_book(
                'Some Title', 'Some Author', '99', 'Some Genre', '123456')
    
    @patch('Controllers.controllers.get_connection')
    def test_list_all_books_returns_none_if_there_arent_books(self, mock_get_connection):
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        mock_cursor.fetchall.return_value = []

        controller = BookController()
        result = controller.list_all_books()

        mock_cursor.execute.assert_called_once_with('SELECT * FROM books')
        self.assertIsNone(result)

    @patch('Controllers.controllers.get_connection')
    def test_list_all_books_returns_list_of_books(self, mock_get_connection):
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        book1 = (1, 'Title', 'Author', 1900, 'Genre', '1234567891')
        book2 = (2, 'Other Title', 'Other Author', 1900, 'Other Genre', '9874562131')
        
        mock_cursor.fetchall.return_value = [book1, book2]

        controller = BookController()
        result = controller.list_all_books()

        mock_cursor.execute.assert_called_once_with('SELECT * FROM books')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], book1)
        self.assertEqual(result[1], book2)

    @patch('Controllers.controllers.get_connection')
    def test_search_book_by_code_returns_the_searched_book(self, mock_get_connection):
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        expected_result = (3, 'Title', 'J.K', 1978, 'Fict', '789456123')
        mock_cursor.fetchone.return_value = expected_result

        controller = BookController()

        result = controller.search_by_book_code('789456123')

        mock_cursor.execute.assert_called_once_with('SELECT * FROM books WHERE isbn_code = %s', ('789456123',))        
        self.assertEqual(result, expected_result)

    @patch('Controllers.controllers.get_connection')
    def test_search_book_by_code_returns_none_if_doesnt_find_the_inputted_book_code(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        mock_cursor.fetchone.return_value = None

        controller = BookController()

        result = controller.search_by_book_code('2223335544')

        mock_cursor.execute.assert_called_once_with('SELECT * FROM books WHERE isbn_code = %s', ('2223335544', ))
        self.assertIsNone(result)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_delete_book_deletes_the_given_book_from_the_db(self, mock_search_by_book_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        controller = BookController()

        mock_search_by_book_code.return_value = (1, 'Title', 'Author', 1900, 'Genre', '456789123')
        result = controller.delete_book('456789123')

        mock_cursor.execute.assert_called_once_with('DELETE FROM books WHERE isbn_code = %s', ('456789123', ))
        self.assertTrue(result)

    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_delete_book_returns_false_if_doesnt_find_the_searched_book(self, mock_search_by_book_code):
        mock_search_by_book_code.return_value = None

        controller = BookController()

        result = controller.delete_book('01010101')

        self.assertFalse(result)
        
    @patch('Controllers.controllers.get_connection')    
    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_update_book_with_valid_data(self, mock_search_by_book_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        returned_book = (1, 'title', 'author', 1980, 'genre', '45678913455')

        controller = BookController()
        mock_search_by_book_code.return_value = returned_book

        result = controller.update_book(returned_book[5], 'Updated title', 'Updated author', 1981, 'Updated genre')
        
        mock_cursor.execute.assert_called_once_with("""
                 UPDATE books SET (title, author, year, genre) = (%s, %s, %s, %s)
                 WHERE isbn_code = %s;
                 """, 
                 ('Updated title', 'Updated author', 1981, 'Updated genre', '45678913455', )
                 )
        self.assertTrue(result)

    @patch('Controllers.controllers.BookController.search_by_book_code')
    def test_update_book_returns_none_when_doesnt_find_the_searched_book(self, mock_search_by_book_code):
        mock_search_by_book_code.return_value = None

        controller = BookController()

        result = controller.update_book('01010101')

        self.assertFalse(result)

    def test_validate_book_fields_raises_value_error_if_any_field_is_invalid(self):
        controller = BookController()

        test_data = [
            ('123465', 'Updated author', 2024,'Updated genre', '11111'),  # title numeric
            ('Updated title', '123456', 2024,'Updated genre', '22222'),  # author numeric
            ('Updated title', 'Updated author', 2024,'123456', '44444'),  # genre numeric

            ('Updated title', 'Updated author', 'ABCD','Updated genre', '33333',),  # year non numeric
            ('Updated title', 'Updated author', 2025, 'Updated genre','33333',),  # year greatter than current year
            ('Updated title', 'Updated author', 99, 'Updated genre','33333',),  # year less than current year
        ]
        for title, author, year, genre, code in test_data:
            with pytest.raises(ValueError):
                controller.validate_book_fields(title, author, year, genre, code)


class TestUserController(unittest.TestCase):

    @patch('Controllers.controllers.get_connection')
    def test_connection_failed(self, mock_get_connection):    
        mock_get_connection.return_value = None

        with pytest.raises(Exception, match="Failed to establish database connection"):
            controller = UserController()

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_register_with_valid_fields(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn        
        mock_find_by_user_code.return_value = None

        controller = UserController()

        result = controller.register_user('Name', 'email@test.com', '11977774444', 1000)

        mock_cursor.execute.assert_called_once_with("INSERT INTO users (name, email, phone, user_code) VALUES (%s, %s, %s, %s);", ('Name', 'email@test.com', '11977774444', 1000))
        self.assertEqual(result, "Success! User registered.")

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_empty_fields_validation(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = None
        controller = UserController()
        
        test_data = [
            ('', 'someemail@test.com', '11912345678', 1000),  # name empty
            ('Other Name', '', '11987654321', 1001),  # email empty
            ('Other Name', 'otheremail@test.com', '', 1002),  # phone empty
            ('Other Name', 'otheremail@test.com', '11987654321', ''),  # user_code empty
        ]
        for name, email, phone, user_code in test_data:
            with pytest.raises(ValueError):
                controller.register_user(name, email, phone, user_code)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_raises_value_error_if_name_and_email_are_numerics(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = None
        controller = UserController()
        
        test_data = [
            ('123456', 'someemail@test.com', '11912345678', 1000),  # name is numeric
            ('Other Name', '123465', '11987654321', 1001)  # email is numeric
        ]
        for name, email, phone, user_code in test_data:
            with pytest.raises(ValueError):
                controller.register_user(name, email, phone, user_code)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_raises_value_error_if_phone_and_user_code_arent_numerics(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = None
        controller = UserController()
        
        test_data = [
            ('Some Name', 'someemail@test.com', '(11)999994444', 1000),
            ('Other Name', 'otheremail@test.com', '11987654321', 'ABCD'),
            ('Other Name', 'otheremail@test.com', '11987654321', '1000'), # user_code type is str
        ]
        for name, email, phone, user_code in test_data:
            with pytest.raises(Exception):
                controller.register_user(name, email, phone, user_code)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_len_of_phone_is_ten_or_eleven(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = None
        controller = UserController()
        
        test_data = [
            ('Some Name', 'someemail@test.com', '119999944444', 1000),  # phone with 12 numbers
            ('Other Name', 'otheremail@test.com', '113333555', 1001),  # phone with 9 numbers
        ]
        for name, email, phone, user_code in test_data:
            with pytest.raises(LenOfPhoneError):
                controller.register_user(name, email, phone, user_code)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_register_user_return_format_email_error_if_it_isnt_valid(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = None
        controller = UserController()
        
        test_data = [
            # ('Some Name', 'someemail@test.com', '11999994444', '1000'), # correct format
            # ('Other Name', 'otheremail@test.com.br', '1133335555', '1001'), # correct format
            ('Some Name', 'someemailtest.com', '11999994444', 1000),
            ('Other Name', 'otheremail@testcombr', '1133335555', 1001),
        ]
        for name, email, phone, user_code in test_data:
            with pytest.raises(EmailFormatError):
                controller.register_user(name, email, phone, user_code)

    @patch("Controllers.controllers.UserController.find_by_user_code")
    @patch("Controllers.controllers.get_connection")
    def test_register_user_duplicated_user_code(self, mock_get_connection, mock_find_by_user_code):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        expected_result = ('Some Name', 'someemail@test.com', '11999994444', 1000)

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = expected_result

        controller = UserController()

        with pytest.raises(DuplicateError):
            controller.register_user('Some Name', 'someemail@test.com', '11999994444', 1000)

    @patch('Controllers.controllers.get_connection')
    def test_list_users_returns_a_list_of_users(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        user1 = ('User One', 'uone@test.com', '12345678910', 1000),
        user2 = ('User Two', 'utwo@test.com', '10987654321', 1001),

        mock_cursor.fetchall.return_value = [user1, user2]

        controller = UserController()

        result = controller.list_users()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users", ())
        self.assertEqual(type(result), list)
        self.assertEqual(result[0], user1)
        self.assertEqual(result[1], user2)

    @patch("Controllers.controllers.get_connection")
    def test_find_by_user_code_returns_a_user(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        expected_result = ('User One', 'uone@test.com', '12345678910', 1000)

        mock_cursor.fetchone.return_value = expected_result

        controller = UserController()
        
        result = controller.find_by_user_code(1000)

        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE user_code = %s;", (1000, ))
        self.assertEqual(result, expected_result)

    @patch("Controllers.controllers.get_connection")
    def test_find_by_user_code_returns_none_if_it_doesnt_exists(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        mock_cursor.fetchone.return_value = None

        controller = UserController()

        result = controller.find_by_user_code(789123)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE user_code = %s;", (789123, ))
        self.assertIsNone(result)

    @patch("Controllers.controllers.UserController.find_by_user_code")
    @patch("Controllers.controllers.get_connection")
    def test_delete_user(self, mock_get_connection, mock_find_by_user_code):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        expected_result = MagicMock()

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = expected_result

        controller = UserController()

        result = controller.delete_user(1000)

        mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE user_code = %s;", (1000, ))
        self.assertTrue(result)

    @patch("Controllers.controllers.UserController.find_by_user_code")
    def test_delete_user_returns_false_if_user_code_doesnt_exists(self, mock_find_by_user_code):

        mock_find_by_user_code.return_value = False

        controller = UserController()

        result = controller.delete_user(97864216)

        self.assertFalse(result)

    @patch('Controllers.controllers.get_connection')
    @patch('Controllers.controllers.UserController.find_by_user_code')
    def test_update_user(self, mock_find_by_user_code, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        expected_result = MagicMock()

        mock_get_connection.return_value = mock_conn    
        mock_find_by_user_code.return_value = expected_result

        controller = UserController()

        result = controller.update_user(2000, 'Updated Name', 'updated@email.com', '11444477777')

        mock_cursor.execute.assert_called_once_with("""
                 UPDATE users SET (name, email, phone) = (%s, %s, %s)
                 WHERE user_code = %s;
                 """, ('Updated Name', 'updated@email.com', '11444477777', 2000, ))
        self.assertTrue(result)

    @patch("Controllers.controllers.UserController.find_by_user_code")
    def test_update_user_returns_none_when_doesnt_find_the_searched_user(self, mock_find_by_user_code):
        mock_find_by_user_code.return_value = None
        controller = UserController()
        result = controller.update_user(2000, 'Updated Name', 'updated@email.com', '11444477777')
        self.assertIsNone(result)

    