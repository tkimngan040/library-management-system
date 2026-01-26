from models.book import Book

class DisplayController:
    @staticmethod
    def get_all_books():
        return Book.get_all_books()
    
    @staticmethod
    def get_book_details(book_id):
        return Book.get_book_by_id(book_id)
    
    @staticmethod
    def get_categories():
        return Book.get_categories()
