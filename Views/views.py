from Controllers.controllers import BookController, UserController
from Exceptions.exceptions import DuplicateError, EmailFormatError, LenOfPhoneError
from prompt_toolkit import prompt
import psycopg2

book_controller = BookController()
user_controller = UserController()

# BOOK VIEWS


def show_menu():
    choice = None
    ipt = input(f'- Type 1 to manage books.\n'
                f'- Type 2 to manage users.\n'
                f'- Type 0 "zero" to exit system.\n'
                f'{'-' * 80}\n')
    print('-' * 85)
    if ipt == '0':
        print('Exiting the system.')
    elif ipt == '1':
        print(f'- To add a new book type 1.\n'
              f'- To list all books type 2.\n'
              f'- To search for a book type 3.\n'
              f'- To update a book type 4.\n'
              f'- To delete a book type 5.')
        print('-' * 85)
        choice = input()
        print('-' * 85)
    elif ipt == '2':
        print(f'- To add a new user type 1.\n'
              f'- To list all users type 2.\n'
              f'- To search for a user type 3.\n'
              f'- To update a user type 4.\n'
              f'- To delete a user type 5')
        print('-' * 85)
        choice = input()
    else:
        print(f'Invalid input!\n'
              f'Please, type "1" to manage books or "2" to manage users')
        print('-' * 85)
    return ipt, choice

def get_book_infos():
    title = input("Book title: ")
    author = input("Author: ")
    year = input("Publication year: ")
    genre = input("Literary genre: ")
    code = input("ISBN code: ")
    print('-' * 85)
    return title, author, year, genre, code

def book_register(controller):
    try:
        title, author, year, genre, code = get_book_infos()
        ret = controller.add_book(title, author, year, genre, code)
        print(ret)
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f'Error: {e}')
    except DuplicateError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def show_books(controller):
    try:
        books = controller.list_all_books()
        if books:
            print("All books list:")
            print()
            for book in sorted(books, reverse=True):
                print(f'ISBN Code: {book[5]:<13} | Title: {book[1]:<20} | Author: {book[2]:<20} |')
        else:
            print('There are no books registered yet')
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def search_book(controller):
    try:
        ipt_code = input('Enter the book ISBN code: ')
        print('-' * 85)
        book = controller.search_by_book_code(ipt_code)
        if book:
            print('Book found:\n')
            print(f'ISBN Code: {book[5]} | Title: {book[1]} | Author: {book[2]} | Publication year: {book[3]} | Genre: {book[4]}')

        else:
            print('Book not found')
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def delete_book(controller):
    try:
        ipt_code = input('Enter the ISBN code of the book you want to delete: ')
        print('-' * 85)
        if not controller.delete_book(ipt_code):
            print("ISBN code doesn't exists.")
        else:
            print("Book deleted.")
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_book(controller):
    try:
        ipt_code = input('Enter the book ISBN code you want to update: ')
        print('-' * 85)
        book = controller.search_by_book_code(ipt_code)
        if book:
                new_title = prompt("Book Title: ", default=book[1]).strip() or book[1]
                new_author = prompt("Author: ", default=book[2]).strip() or book[2]
                new_year = prompt("Publication Year: ", default=str(book[3])).strip() or book[3]
                new_genre = prompt("Literary genre: ", default=book[4]).strip() or book[4]
                print('-' * 85)
                controller.update_book(ipt_code, new_title, new_author, new_year, new_genre)
                print('Book updated')
        else:
            print("Book not found")
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# USER VIEWS

def get_user_infos():
    name = input("Name: ")
    email = input("E-mail: ")
    phone = input("Phone number: ")
    user_code = input("User code: ")
    print('-' * 85)
    return name, email, phone, user_code

def user_register(controller):
    try:
        name, email, phone, user_code = get_user_infos()
        controller.register_user(name, email, phone, user_code)
        print('User registered!')
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
    except ValueError as e:
        print(f'Error: {e}')
    except EmailFormatError as e:
        print(f'Error: {e}')
    except LenOfPhoneError as e:
        print(f'Error: {e}')
    except TypeError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f"Error {e}")

def show_users(controller):
    try:
        users = controller.list_users()
        if users:
            for user in users:
                print(f'User code: {user[4]:<6} | Name: {user[1]:<30} | Email: {user[2]:<20} |')
        else:
            print('There are no users registered yet')
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except Exception as e:
        print(f"Error: {e}")

def search_user(controller):
    ipt_code = input('Enter the user code: ')
    print('-' * 85)
    if not ipt_code.isnumeric():
        print('User code must contain just numbers')
    else:
        try:
            user = controller.find_by_user_code(ipt_code)
            if user:
                print(f'User code: {user[4]} | Name: {user[1]} | Email: {user[2]} | Phone number: {user[3]}')
            else:
                print('User not found')
        except psycopg2.Error as db_error:
            print(f"Database error: {db_error}")
        except Exception as e:
            print(f"Error: {e}")

def delete_user(controller):
    try:
        ipt_code = input('Enter the user code you want to delete: ')
        print('-' * 85)
        if not controller.delete_user(ipt_code):
            print("User not found.")
        else:
            print("User deleted.")
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
    except Exception as e:
        print(f'Error {e}')

def update_user(controller):
    try:
        ipt_code = int(input('Enter the user code you want to update: '))
        print('-' * 85)
        user = controller.find_by_user_code(ipt_code)
        if user:
            new_name = prompt("Name: ", default=user[1]).strip() or user[1]
            new_email = prompt("E-mail: ", default=user[2]).strip() or user[2]
            new_phone = prompt("Phone number: ", default=user[3]).strip() or user[3]
            print('-' * 85)
            controller.update_user(ipt_code, new_name, new_email, new_phone)
            print('User updated')
        else:
            print("User not found")
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
    except ValueError:
        print('-' * 85)
        print('User code must contain just numbers')
