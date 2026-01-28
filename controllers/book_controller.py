from tkinter import messagebox
from models.book import Book
from models.borrow import Borrow
from views.book_view import BookView



class BookController:
    def __init__(self, app):
        self.app = app
        self.book_model = Book()
        self.borrow_model = Borrow()


    def get_book_detail(self, book_id):
        row = self.book_model.get_by_id(book_id)
        if not row:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "category": row[3],
            "total": row[4],
            "available": row[5]
        }
    def show_books(self):
        self.app.clear_screen()
        self.app.render_header("Books")
        books = self.book_model.get_all()
        BookView(self.app.root, self, books).pack(fill="both", expand=True)

    def borrow_book(self, book_id):
        user = self.app.current_user

        if not user:
            messagebox.showwarning(
                "Login required",
                "Please login to borrow books"
            )
            self.app.auth.show_login()
            return False

        # bắt user role
        if user.role != "user":
            messagebox.showerror(
                "Permission denied",
                "Only members can borrow books"
            )
            return False

        book = self.book_model.get_by_id(book_id)
        if not book or book[5] <= 0:
            messagebox.showinfo(
                "Unavailable",
                "This book is not available"
            )
            return False

        self.borrow_model.create(user.id, book_id)
        self.book_model.decrease_available(book_id)

        messagebox.showinfo("Success", "Borrow book successfully!")
        return True

