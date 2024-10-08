class Book():
    def __init__(self, title: str, author: str, year: int, genre: str, isbn_code: str) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn_code = isbn_code
    
    def show_info(self):
        return f' ISBN code: {self.isbn_code} | Title: {self.title} | Author: {self.author} | Publication Year: {self.year} | Genre: {self.genre}'
            

class User():
    def __init__(self, name: str, email: str, phone: str, user_code: int) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.user_code = user_code

    def show_info(self):
        return f' User code: {self.user_code} | Name: {self.name} | E-mail: {self.email} | Phone: {self.phone}'
