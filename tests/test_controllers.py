from Controllers.controllers import BookController, UserController
import pytest



def test_add_book_with_valid_data():
    controller = BookController()
    controller.add_book('Some Title', 'Some Author', '1234', 'Some Genre', '123456')
    assert len(controller.db) == 1

    added_book = controller.db[0]
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
def test_add_book_raises_ValueError_if_any_field_is_empty(title, author, year, genre, code):
    controller = BookController()
    with pytest.raises(ValueError):
        controller.add_book(title, author, year, genre, code)        
