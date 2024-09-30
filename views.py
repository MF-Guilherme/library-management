from controllers import BookController, UserController
from prompt_toolkit import prompt

book_controller = BookController()
user_controller = UserController()

# BOOK VIEWS

def show_menu():
    choice = None
    ipt = input(f'- Type 1 to manage books.\n'
                f'- Type 2 to manage users.\n'
                f'- Type 0 "zero" to exit system.\n'
                f'{'-' * 50}\n')
    print('-' * 50)
    if ipt == '0':
        print('Exiting the system.')
    elif ipt == '1':
        print(f'- To add a new book type 1.\n'
              f'- To list all books type 2.\n'
              f'- To search for a book type 3.\n'
              f'- To update a book type 4.\n'
              f'- To delete a book type 5.')
        print('-' * 50)
        choice = input()
        print('-' * 50)
    elif ipt == '2':
        print(f'- To add a new user type 1.\n'
              f'- To list all users type 2.\n'
              f'- To search for a user type 3.\n'
              f'- To update a user type 4.\n'
              f'- To delete a user type 5')
        print('-' * 50)
        choice = input()
    else:
        print(f'Invalid input!\n'
              f'Please, type "1" to manage books or "2" to manage users')
        print('-' * 50)
    return ipt, choice

def get_book_infos():
    title = input("Book title: ")
    author = input("Author: ")
    year = input("Publication year: ")
    genre = input("Literary genre: ")
    code = input("ISBN code: ")
    print('-' * 50)
    return title, author, year, genre, code

def book_register(controller):
    title, author, year, genre, code = get_book_infos()
    controller.add_book(title, author, year, genre, code)
    print('Book registered!')

def show_books(controller):
    books = controller.list_books()
    if books:
        for book in books:
            print(f'Title: {book.title} | Author: {book.author} | ISBN: {book.code}')
    else: 
        print('There are no books registered yet')

def search_book(controller):
    ipt_code = input('Enter the book ISBN code: ')
    print('-' * 50)
    book = controller.search_by_book_code(ipt_code)
    if book:
        print(f'Title: {book.title} | Author: {book.author} | ISBN: {book.code}')
    else:
        print('Book not found')
    
def delete_book(controller):
    ipt_code = input('Enter the ISBN code of the book you want to delete: ')
    print('-' * 50)
    if not controller.delete_book(ipt_code):
        print("ISBN code doesn't exists.")
    else:
        print("Book deleted.")

def update_book(controller):
    ipt_code = input('Enter the book ISBN code you want to update: ')
    print('-' * 50)
    book = controller.search_by_book_code(ipt_code)
    if book:
        new_title = prompt("Book Title: ", default=book.title).strip() or book.title
        new_author = prompt("Author: ", default=book.author).strip() or book.author
        new_year = prompt("Publication Year: ", default=book.year).strip() or book.year
        new_genre = prompt("Literary genre: ", default=book.genre).strip() or book.genre
        print('-' * 50)
        controller.update_book(ipt_code, new_title, new_author, new_year, new_genre)
        print('Book updated')
    else:
        print("Book not found")

# USER VIEWS
    
def get_user_infos():
    name = input("Name: ")
    email = input("E-mail: ")
    phone = input("Phone number: ")
    user_code = input("User code: ")
    print('-' * 50)
    return name, email, phone, user_code

def user_register(controller):
    name, email, phone, user_code = get_user_infos()
    controller.register_user(name, email, phone, user_code)
    print('User registered!')

def show_users(controller):
    users = controller.list_users()
    if users:
        for user in users:
            print(f'Name: {user.name} | Email: {user.email} | User code: {user.user_code}')
    else: 
        print('There are no users registered yet')

def search_user(controller):
    ipt_code = input('Enter the user code: ')
    print('-' * 50)
    user = controller.find_by_user_code(ipt_code)
    if user:
        print(f' User code: {user.user_code} | Name: {user.name} | Email: {user.email} | Phone number: {user.phone}')
    else:
        print('User not found')
    
def delete_user(controller):
    ipt_code = input('Enter the user code you want to delete: ')
    print('-' * 50)
    if not controller.delete_user(ipt_code):
        print("User not found.")
    else: 
        print("User deleted.")

def update_user(controller):
    ipt_code = input('Enter the user code you want to update: ')
    print('-' * 50)
    user = controller.find_by_user_code(ipt_code)
    if user:
        new_name = prompt("Name: ", default=user.name).strip() or user.name
        new_email = prompt("E-mail: ", default=user.email).strip() or user.email
        new_phone = prompt("Phone number: ", default=user.phone).strip() or user.phone
        print('-' * 50)
        controller.update_user(ipt_code, new_name, new_email, new_phone)
        print('User updated')
    else:
        print("User not found")
