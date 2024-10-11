from Models.models import User
from Controllers.controllers import BookController, UserController
from Exceptions.exceptions import DuplicateError, LenOfPhoneError, EmailFormatError
from unittest.mock import patch, MagicMock
import pytest, unittest


class TestBookController(unittest.TestCase):

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

#     def test_delete_book_deletes_the_given_book_from_the_db(self, setup_book):
#         book = setup_book.search_by_book_code('123456')
#         setup_book.delete_book(book.isbn_code)
#         list_books = setup_book.list_books()
#         assert book not in list_books

#     def test_delete_book_returns_false_if_doesnt_find_the_searched_book(self, setup_book):
#         book_code = '111111'
#         ret = setup_book.delete_book(book_code)
#         assert ret is False

#     def test_update_book_with_valid_data(self, setup_book):
#         book = setup_book.search_by_book_code('123456')
#         update_return = setup_book.update_book(
#             book.isbn_code, 'Updated title', 'Updated author', '2024', 'Updated genre')
#         updated_book = setup_book.search_by_book_code('123456')

#         assert update_return is True
#         assert updated_book.title == 'Updated title'
#         assert updated_book.author == 'Updated author'
#         assert updated_book.year == '2024'
#         assert updated_book.genre == 'Updated genre'

#     @pytest.mark.parametrize(
#         "title, author, year, genre, code",
#         [
#             ('123465', 'Updated author', '2024',
#              'Updated genre', '11111'),  # title numeric
#             ('Updated title', '123456', '2024',
#              'Updated genre', '22222'),  # author numeric
#             ('Updated title', 'Updated author', '2024',
#              '123456', '44444'),  # genre numeric

#             ('Updated title', 'Updated author', 'ABCD',
#              'Updated genre', '33333',),  # year non numeric
#             ('Updated title', 'Updated author', '2025', 'Updated genre',
#              '33333',),  # year greatter than current year
#             ('Updated title', 'Updated author', '99', 'Updated genre',
#              '33333',),  # year less than current year
#         ]
#     )
#     def test_update_book_raises_ValueError_when_a_field_fails_data_validation(self, setup_books_update, title, author, year, genre, code):
#         book = setup_books_update.search_by_book_code(code)
#         assert book in setup_books_update.list_books(), "book must be register in database"

#         with pytest.raises(ValueError):
#             setup_books_update.update_book(code, title, author, year, genre)

#     def test_update_book_returns_none_when_doesnt_find_the_searched_book(self, setup_books_update):
#         update_return = setup_books_update.update_book(
#             '999999')  # non-existent code
#         assert update_return is None


# class TestUserController():

#     @pytest.fixture
#     def user_controller(self):
#         return UserController()

#     @pytest.fixture
#     def setup_user(self, user_controller):
#         # name, email, phone, user_code
#         user_controller.register_user(
#             'Some Name', 'someemail@test.com', '11912345678', '1000')
#         user_controller.register_user(
#             'Other Name', 'otheremail@test.com', '1133334444', '1001')
#         return user_controller

#     def test_register_user_register_with_valid_fields(self, user_controller):
#         user_controller.register_user(
#             'Some Name', 'someemail@test.com', '11912345678', '1000')
#         user = user_controller.list_users()[0]
#         assert user.name == 'Some Name'
#         assert user.email == 'someemail@test.com'
#         assert user.phone == '11912345678'
#         assert user.user_code == '1000'

#     @pytest.mark.parametrize(
#         "name, email, phone, user_code",
#         [
#             ('', 'someemail@test.com', '11912345678', '1000'),  # name empty
#             ('Other Name', '', '11987654321', '1001'),  # email empty
#             ('Other Name', 'otheremail@test.com', '', '1002'),  # phone empty
#             ('Other Name', 'otheremail@test.com',
#              '11987654321', ''),  # user_code empty
#         ]
#     )
#     def test_register_user_empty_fields_validation(self, user_controller, name, email, phone, user_code):
#         with pytest.raises(ValueError):
#             user_controller.register_user(name, email, phone, user_code)

#     @pytest.mark.parametrize(
#         "name, email, phone, user_code",
#         [
#             ('123456', 'someemail@test.com',
#              '11912345678', '1000'),  # name is numeric
#             ('Other Name', '123465', '11987654321', '1001')  # email is numeric
#         ]
#     )
#     def test_register_user_raises_value_error_if_name_and_email_are_numerics(self, user_controller, name, email, phone, user_code):
#         with pytest.raises(ValueError):
#             user_controller.register_user(name, email, phone, user_code)

#     @pytest.mark.parametrize(
#         "name, email, phone, user_code",
#         [
#             ('Some Name', 'someemail@test.com', '(11)999994444', '1000'),
#             ('Other Name', 'otheremail@test.com', '11987654321', 'CODE1234')
#         ]
#     )
#     def test_register_user_raises_value_error_if_phone_and_user_code_arent_numerics(self, user_controller, name, email, phone, user_code):
#         with pytest.raises(ValueError):
#             user_controller.register_user(name, email, phone, user_code)

#     @pytest.mark.parametrize(
#         "name, email, phone, user_code",
#         [
#             ('Some Name', 'someemail@test.com',
#              '119999944444', '1000'),  # phone with 12 numbers
#             ('Other Name', 'otheremail@test.com',
#              '113333555', '1001'),  # phone with 9 numbers
#         ]
#     )
#     def test_register_user_len_of_phone_is_ten_or_eleven(self, user_controller, name, email, phone, user_code):
#         with pytest.raises(LenOfPhoneError):
#             user_controller.register_user(name, email, phone, user_code)

#     @pytest.mark.parametrize(
#         "name, email, phone, user_code",
#         [
#             # ('Some Name', 'someemail@test.com', '11999994444', '1000'), # correct format
#             # ('Other Name', 'otheremail@test.com.br', '1133335555', '1001'), # correct format
#             ('Some Name', 'someemailtest.com', '11999994444', '1000'),
#             ('Other Name', 'otheremail@testcombr', '1133335555', '1001'),
#         ]
#     )
#     def test_register_user_return_format_email_error_if_it_isnt_valid(self, user_controller, name, email, phone, user_code):
#         with pytest.raises(EmailFormatError):
#             user_controller.register_user(name, email, phone, user_code)


#     def test_register_user_duplicated_user_code(self, setup_user):
#         with pytest.raises(DuplicateError):
#             setup_user.register_user('Some Name', 'someemail@test.com', '11999994444', '1000')

#     def test_list_users_returns_a_list_of_users(self, setup_user):
#         users = setup_user.list_users()

#         assert type(setup_user.list_users()) == list
#         assert isinstance(users[0], User)
#         assert isinstance(users[1], User)

#     def test_find_by_user_code_returns_a_user(self, setup_user):
#         user1 = setup_user.find_by_user_code('1000')
#         user2 = setup_user.find_by_user_code('1001')

#         assert isinstance(user1, User)
#         assert user1.name == 'Some Name'
#         assert user1.email == 'someemail@test.com'
#         assert user1.phone == '11912345678'

#         assert isinstance(user2, User)
#         assert user2.name == 'Other Name'
#         assert user2.email == 'otheremail@test.com'
#         assert user2.phone == '1133334444'

#     def test_find_by_user_code_returns_none_if_it_doesnt_exists(self, setup_user):
#         assert setup_user.find_by_user_code('123465') is None

#     def test_delete_user(self, setup_user):
#         delete_code = '1000'
#         assert setup_user.find_by_user_code(delete_code) in setup_user.db
#         assert setup_user.delete_user(delete_code) is True
#         assert setup_user.find_by_user_code(delete_code) not in setup_user.db
    
#     def test_delete_user_returns_false_if_user_code_doesnt_exists(self, setup_user):
#         delete_code = '123456'
#         assert setup_user.delete_user(delete_code) is False

#     def test_update_user(self, setup_user):
#         user = setup_user.find_by_user_code('1000')
#         update_return = setup_user.update_user(user.user_code, 'Updated name', 'updatedemail@test.com', '11777775555')
#         updated_user = setup_user.find_by_user_code('1000')

#         assert update_return is True
#         assert updated_user.name == 'Updated name'
#         assert updated_user.email == 'updatedemail@test.com'
#         assert updated_user.phone == '11777775555'

#     @pytest.mark.parametrize(
#         "user_code, name, email, phone",
#         [
#             ('1000', '123456', 'updatedemail@test.com','11999994444'),  # name numeric
#             ('1001', 'Update Name', '123456','11999994444'),  # email numeric
#             ('1000', 'Update Name', 'updatedemail','phone123456'),  # phone non numeric
#             ('1001', '', 'updatedemail','phone123456'),  # name empty
#         ]
#     )
#     def test_update_user_raises_value_error_when_a_field_fails_in_data_validation(self, setup_user, user_code, name, email, phone):
#         with pytest.raises(ValueError):
#             setup_user.update_user(user_code, name, email, phone)

#     def test_update_user_returns_none_when_doesnt_find_the_searched_user(self, setup_user):
#         update_return = setup_user.update_user('999999')  # non-existent user code
#         assert update_return is None
