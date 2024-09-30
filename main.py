from Views.views import book_controller, user_controller
import Views.views as views

book_options = {
    '1': views.book_register,
    '2': views.show_books,
    '3': views.search_book,
    '4': views.update_book,
    '5': views.delete_book
}

user_options = {
    '1': views.user_register,
    '2': views.show_users,
    '3': views.search_user,
    '4': views.update_user,
    '5': views.delete_user
}

if __name__ == "__main__":
    while True:
        ipt, choice = views.show_menu()
        if ipt == '0':
            break
        elif ipt == '1':
            try:
                book_options[choice]()
            except TypeError:
                book_options[choice](book_controller)
                print('-' * 50)
            except KeyError:
                print('Insert a valid option.')
                print('-' * 50)
                pass
        elif ipt == '2':
            try:
                user_options[choice]()
            except TypeError:
                user_options[choice](user_controller)
                print('-' * 50)
            except KeyError:
                print('Insert a valid option.')
                print('-' * 50)
                pass


        