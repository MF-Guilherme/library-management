from Controllers.controllers import BookController, UserController
from Exceptions.exceptions import DuplicateBookError
import pytest

class TestBookController():
    
    @pytest.fixture
    def book_controller(self):
        return BookController()
     
    @pytest.fixture
    def setup_book(self, book_controller):
        book_controller.add_book('Some Title', 'Some Author', '1900', 'Some Genre', '123456')
        book_controller.add_book('Another Title', 'Another Author', '2000', 'Another Genre', '789465')
        return book_controller

    @pytest.fixture
    def setup_books_update(self, book_controller):
        book_controller.add_book('Original title', 'Original author', '1900', 'Original genre', '11111')
        book_controller.add_book('Original title', 'Original author', '1900', 'Original genre', '22222')
        book_controller.add_book('Original title', 'Original author', '1900', 'Original genre', '33333')
        book_controller.add_book('Original title', 'Original author', '1900', 'Original genre', '44444')
        return book_controller
        
    def test_add_book_with_valid_data(self, setup_book):
        controller = setup_book    
        assert len(controller.db) == 2

        added_book = controller.db[0]
        assert added_book.title == 'Some Title'
        assert added_book.author == 'Some Author'
        assert added_book.year == '1900'
        assert added_book.genre == 'Some Genre'
        assert added_book.code == '123456'

        added_book = controller.db[1]
        assert added_book.title == 'Another Title'
        assert added_book.author == 'Another Author'
        assert added_book.year == '2000'
        assert added_book.genre == 'Another Genre'
        assert added_book.code == '789465'

    def test_add_book_raises_duplicate_book_error_when_isbn_code_alredy_registered(self, setup_book):
        with pytest.raises(DuplicateBookError):
            setup_book.add_book('Some Title', 'Some Author', '1900', 'Some Genre', '789465')

    @pytest.mark.parametrize(
            "title, author, year, genre, code",
            [
                ('', 'Some Author', '1234', 'Some Genre', '123456'), # title is empty
                ('Some Author', '', '1234', 'Some Genre', '123456'), # author is empty
                ('Some Author', 'Some Author', '', 'Some Genre', '123456'), # year is empty
                ('Some Author', 'Some Author', '1234', '', '123456'), # genre is empty
                ('Some Author', 'Some Author', '1234', 'Some Genre', '') # code is empty
            ]
    )
    def test_add_book_raises_ValueError_if_any_field_is_empty(self, book_controller, title, author, year, genre, code):
        with pytest.raises(ValueError):
            book_controller.add_book(title, author, year, genre, code)

    @pytest.mark.parametrize(
            "title, author, year, genre, code",
            [
                ('Some Title', 'Some Author', 'ABCD', 'Some Genre', '12345'), # year isn't numeric
                ('Some Title', 'Some Author', '1900', 'Some Genre', 'ABCD'), # code isn't numeric
                ('Some Title', 'Some Author', 'ABCD', 'Some Genre', 'BCDA'), # year and code aren't numeric
            ]
    )
    def test_add_book_raises_ValueError_if_year_or_book_are_not_numeric(self, book_controller, title, author, year, genre, code):
        with pytest.raises(ValueError):
            book_controller.add_book(title, author, year, genre, code)

    @pytest.mark.parametrize(
            "title, author, year, genre, code",
            [
                ('123456', 'Some Author', '1900', 'Some Genre', '12345'), # title isn't string
                ('Some Title', '123456', '1900', 'Some Genre', '12345'), # author isn't string
                ('Some Title', 'Some Author', '1900', '123456', '12345'), # genre isn't string
            ]
    )
    def test_add_book_raises_ValueError_if_title_author_or_genre_are_not_strings(self, book_controller, title, author, year, genre, code):
        with pytest.raises(ValueError):
            book_controller.add_book(title, author, year, genre, code)

    def test_add_book_raises_ValueError_if_year_doesnt_less_than_or_equal_current_year(self, book_controller):
        with pytest.raises(ValueError):
            book_controller.add_book('Some Title', 'Some Author', '2025', 'Some Genre', '123456')

    def test_add_book_raises_ValueError_if_digits_in_year_field_are_less_than3(self, book_controller):
        with pytest.raises(ValueError):
            book_controller.add_book('Some Title', 'Some Author', '99', 'Some Genre', '123456')
    
    def test_list_books_returns_empty_list_when_no_books_are_added(self, book_controller):
        assert book_controller.list_books() == [], "Should return an empty list"
    
    def test_list_books_returns_list_of_books_after_adding_books(self, setup_book):
        book1 = setup_book.search_by_book_code('123456')
        book2 = setup_book.search_by_book_code('789465')
        assert setup_book.list_books() == [book1, book2], "The books list does not contain the expected books"

    def test_search_book_by_code_returns_the_searched_book(self, setup_book):
        book = setup_book.search_by_book_code('789465')
        assert setup_book.list_books()[1] == book

    def test_search_book_by_code_returns_none_if_doesnt_find_the_inputted_book_code(self, setup_book):
        book = setup_book.search_by_book_code('456123')
        assert book is None
        
    def test_delete_book_deletes_the_given_book_from_the_db(self, setup_book):
        book = setup_book.search_by_book_code('123456')
        setup_book.delete_book(book.code)
        list_books = setup_book.list_books()
        assert book not in list_books

    def test_delete_book_returns_false_if_doesnt_find_the_searched_book(self, setup_book):
        book_code = '111111'
        ret = setup_book.delete_book(book_code)
        assert ret is False

    def test_update_book_with_valid_data(self, setup_book):
        book = setup_book.search_by_book_code('123456')
        update_return = setup_book.update_book(book.code, 'Updated title', 'Updated author', '2024', 'Updated genre')
        updated_book = setup_book.search_by_book_code('123456')
        
        assert update_return is True
        assert updated_book.title == 'Updated title'
        assert updated_book.author == 'Updated author'
        assert updated_book.year == '2024'
        assert updated_book.genre == 'Updated genre'

    @pytest.mark.parametrize(
            "title, author, year, genre, code",
            [
                ('123465', 'Updated author', '2024', 'Updated genre', '11111'), # title numeric
                ('Updated title', '123456', '2024', 'Updated genre', '22222'), # author numeric 
                ('Updated title', 'Updated author', '2024', '123456', '44444'), # genre numeric

                ('Updated title', 'Updated author', 'ABCD', 'Updated genre', '33333',), # year non numeric
                ('Updated title', 'Updated author', '2025', 'Updated genre', '33333',), # year greatter than current year
                ('Updated title', 'Updated author', '99', 'Updated genre', '33333',), # year less than current year
            ]
    )
    def test_update_book_raises_ValueError_when_a_field_fails_data_validation(self, setup_books_update, title, author, year, genre, code):
        book = setup_books_update.search_by_book_code(code)
        assert book in setup_books_update.list_books(), "book must be register in database"

        with pytest.raises(ValueError):
            setup_books_update.update_book(code, title, author, year, genre)

    def test_update_book_returns_none_when_doesnt_find_the_searched_book(self, setup_books_update):
        update_return = setup_books_update.update_book('999999') # non-existent code
        assert update_return is None


class TestUserController():
    
    @pytest.fixture
    def user_controller(self):
        return UserController()
     
    @pytest.fixture
    def setup_user(self, user_controller):
        # name, email, phone, user_code
        user_controller.register_user('Some Name', 'someemail@test.com', '11912345678', '1000')
        user_controller.register_user('Other Name', 'otheremail@test.com', '11987654321', '1001')
        return user_controller
    
    @pytest.mark.parametrize(
            "name, email, phone, user_code",
            [
                ('123456', 'someemail@test.com', '11912345678', '1000'), # name is numeric
                ('Other Name', '123465', '11987654321', '1001') # email is numeric
            ]
    )
    def test_register_user_raises_value_error_if_name_and_email_are_numerics(self, user_controller, name, email, phone, user_code):
        with pytest.raises(ValueError):
            user_controller.register_user(name, email, phone, user_code)