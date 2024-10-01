from Controllers.controllers import BookController, UserController
import pytest

class TestBookController():
    
    def setup_method(self):
        self.controller = BookController()
        

    def test_add_book_with_valid_data(self):
        self.controller.add_book('Some Title', 'Some Author', '1234', 'Some Genre', '123456')
        assert len(self.controller.db) == 1

        added_book = self.controller.db[0]
        assert added_book.title == 'Some Title'
        assert added_book.author == 'Some Author'
        assert added_book.year == '1234'
        assert added_book.genre == 'Some Genre'
        assert added_book.code == '123456'


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
    def test_add_book_raises_ValueError_if_any_field_is_empty(self, title, author, year, genre, code):
        with pytest.raises(ValueError):
            self.controller.add_book(title, author, year, genre, code)        


    @pytest.mark.parametrize(
            "title, author, year, genre, code",
            [
                ('Some Title', 'Some Author', 'ABCD', 'Some Genre', '12345'), # year isn't numeric
                ('Some Title', 'Some Author', '1900', 'Some Genre', 'ABCD'), # code isn't numeric
            ]
    )
    def test_add_book_raises_ValueError_if_year_or_book_are_not_numeric(self, title, author, year, genre, code):
        with pytest.raises(ValueError):
            self.controller.add_book(title, author, year, genre, code)