import tkinter as tk
from tkinter import ttk, messagebox

class BookView(tk.Frame):
    def __init__(self, master, controller, books):
        super().__init__(master)
        self.controller = controller
        self.books = books

        # ======================
        # TITLE
        # ======================
        tk.Label(
            self,
            text="Book Library",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        # ======================
        # TABLE
        # ======================
        columns = ("title", "author", "category", "status", "actions")

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )

        self.table.heading("title", text="Book Title")
        self.table.heading("author", text="Author")
        self.table.heading("category", text="Category")
        self.table.heading("status", text="Status")
        self.table.heading("actions", text="Actions")

        self.table.column("title", width=220)
        self.table.column("author", width=160)
        self.table.column("category", width=120)
        self.table.column("status", width=100, anchor="center")
        self.table.column("actions", width=120, anchor="center")

        self.table.pack(fill="both", expand=True, padx=15, pady=10)

        self.load_books()

        # Click vào cột Actions
        self.table.bind("<ButtonRelease-1>", self.on_click)

    def load_books(self):
        for book in self.books:
            book_id = book[0]
            status = "Available" if book[4] > 0 else "Borrowed"

            self.table.insert(
                "",
                "end",
                iid=book_id,
                values=(
                    book[1],  # Title
                    book[2],  # Author
                    book[3],  # Category
                    status,
                    "View Details"
                )
            )

    def on_click(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.table.identify_column(event.x)
        row = self.table.identify_row(event.y)

        # Cột Actions là cột thứ 5
        if column == "#5" and row:
            self.open_detail_popup(row)

    def open_detail_popup(self, book_id):
        book = self.controller.get_book_detail(book_id)
        if not book:
            return

        popup = tk.Toplevel(self)
        popup.title("Book Details")
        popup.geometry("400x300")
        popup.resizable(False, False)

        tk.Label(popup, text=book["title"], font=("Arial", 14, "bold")).pack(pady=10)

        info = [
            f"Author: {book['author']}",
            f"Category: {book['category']}",
            f"Total Copies: {book['total']}",
            f"Available Copies: {book['available']}",
            f"Status: {'Available' if book['available'] > 0 else 'Borrowed'}"
        ]

        for line in info:
            tk.Label(popup, text=line, anchor="w").pack(fill="x", padx=20, pady=2)

        tk.Button(
            popup,
            text="Borrow Book",
            command=lambda: self.borrow_from_popup(book_id, popup)
        ).pack(pady=15)

    def borrow_from_popup(self, book_id, popup):
        if self.controller.borrow_book(book_id):
            popup.destroy()
            self.table.delete(*self.table.get_children())
            self.reload_books()

    def reload_books(self):
        # Xoá toàn bộ dòng cũ
        for row in self.table.get_children():
            self.table.delete(row)

        # Lấy data mới từ DB
        books = self.controller.book_model.get_all()

        for book in books:
            status = "Available" if book[5] > 0 else "Borrowed"

            self.table.insert(
                "",
                "end",
                iid=book[0],
                values=(
                    book[1],
                    book[2],
                    book[3],
                    status,
                    "View Details"
                )
            )
