class Book():
    def __init__(self, title, author, year, genre, code) -> None:
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.code = code
    
    def show_info(self):
        return f'Title: {self.title} | Author: {self.author} | Publication Year: {self.year} | Genre: {self.genre} | ISBN code: {self.code}'
            

class User():
    def __init__(self, name, email, phone, user_code) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.user_code = user_code

    def show_info(self):
        return f'Name: {self.name} | E-mail: {self.email} | Phone: {self.phone} | User code: {self.user_code}'
