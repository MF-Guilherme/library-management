class DuplicateBookError(Exception):
    """Raised when a book with the same code is being added"""
    def __init__(self, code, entity="Book"):
        self.code = code
        self.entity = entity
        self.message = f"{self.entity} with code {self.code} already exists."
        super().__init__(self.message)

class LenOfPhoneError(Exception):
    """Raised when the phone number doesn't have 10 or 11 characters"""
    def __init__(self):
        self.message = "The phone number must contain 10 or 11 numbers without any other characters."
        super().__init__(self.message)

class EmailFormatError(Exception):
    def __init__(self, email):
        self.email = email
        self.message = f"{self.email} is not a valid email"
        super().__init__(self.message)