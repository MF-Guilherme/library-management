class DuplicateBookError(Exception):
    """Raised when a book with the same code is being added"""
    def __init__(self, code, entity="Book"):
        self.code = code
        self.entity = entity
        self.message = f"{self.entity} with code {self.code} already exists."
        super().__init__(self.message)