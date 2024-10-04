from Controllers.controllers import BookController, UserController
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
            "title, author, year, genre, code, expected_title, expected_author, expected_year, expected_genre",
            [
                ('', 'Updated author', '2024', 'Updated genre', '11111', 'Original title', 'Updated author', '2024', 'Updated genre' ), # title empty
                ('Updated title', '', '2024', 'Updated genre', '22222', 'Updated title', 'Original author', '2024', 'Updated genre'), # author empty 
                ('Updated title', 'Updated author', '', 'Updated genre', '33333', 'Updated title', 'Updated author', '1900', 'Updated genre'), # year empty
                ('Updated title', 'Updated author', '2024', '', '44444', 'Updated title', 'Updated author', '2024', 'Original genre'), # genre empty
            ]
    )
    def test_update_book_doesnt_changes_the_field_when_its_omitted(self, setup_books_update, title, author, year, genre, code, expected_title, expected_author, expected_year, expected_genre):
        book = setup_books_update.search_by_book_code(code)
        assert book in setup_books_update.list_books(), "book must be register in database"

        setup_books_update.update_book(code, title, author, year, genre)

        upated_book = setup_books_update.search_by_book_code(code)

        assert upated_book.title == expected_title, f"Title should be {expected_title}"
        assert upated_book.author == expected_author, f"Author should be {expected_author}"
        assert upated_book.year == expected_year, f"Year should be {expected_year}"
        assert upated_book.genre == expected_genre, f"Genre should be {expected_genre}"
