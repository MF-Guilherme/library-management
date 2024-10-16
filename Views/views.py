from Controllers.controllers import BookController, UserController
from Exceptions.exceptions import DuplicateError, EmailFormatError, LenOfPhoneError
from prompt_toolkit import prompt
from tabulate import tabulate
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
        show_books(controller)
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
            books_without_id = [row[1:] for row in books]
            headers = ['Title', 'Author', 'Publication year', 'Genre', 'ISBN Code']
            print(tabulate(sorted(books_without_id, reverse=True), showindex=False, headers=headers, tablefmt="grid"))
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
            book_without_id = [book[1:]]
            headers = ['Title', 'Author', 'Publication year', 'Genre', 'ISBN Code']
            print(tabulate(book_without_id, headers=headers, tablefmt="grid"))
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
            show_books(controller)
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
                show_books(controller)
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
    user_code = int(input("User code: "))
    print('-' * 85)
    return name, email, phone, user_code

def user_register(controller):
    try:
        name, email, phone, user_code = get_user_infos()
        controller.register_user(name, email, phone, user_code)
        print('User registered!')
        show_users(controller)
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
            users_reordered = [(row[4], row[1], row[2], row[3]) for row in users]
            headers = ['User Code', 'Name', 'E-mail', 'Phone']
            print(tabulate(sorted(users_reordered, reverse=True), showindex=False, headers=headers, tablefmt="grid"))
        else:
            print('There are no users registered yet')
    except psycopg2.Error as db_error:  
        print(f"Database error: {db_error}")
    except Exception as e:
        print(f"Error: {e}")

def search_user(controller):
    try:
        ipt_code = input('Enter the user code: ')
        print('-' * 85)
        if not ipt_code.isnumeric():
            print('User code must contain just numbers')
        else:
            user = controller.find_by_user_code(ipt_code)
            if user:
                user = [user]
                user_reordered = [(row[4], row[1], row[2], row[3]) for row in user]
                headers = ['User Code', 'Name', 'E-mail', 'Phone']
                print(tabulate(sorted(user_reordered, reverse=True), showindex=False, headers=headers, tablefmt="grid"))
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
            show_users(controller)
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
            show_users(controller)
        else:
            print("User not found")
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
    except ValueError:
        print('-' * 85)
        print('User code must contain just numbers')
