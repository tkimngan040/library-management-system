from models.book import Book

class AdminBookController:
    def __init__(self):
        self.model = Book()

    def get_books(self):
        return self.model.get_all()

    def add_book(self, title, author, category, total):
        self.model.create(title, author, category, total)

    def delete_book(self, book_id):
        self.model.delete(book_id)
