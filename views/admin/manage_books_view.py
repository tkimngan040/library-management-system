import tkinter as tk
from tkinter import ttk, messagebox

class ManageBooksView(tk.Frame):
    def __init__(self, parent, app, controller):
        super().__init__(parent)
        self.app = app
        self.controller = controller

        self.table = ttk.Treeview(
            self,
            columns=("title", "author", "category", "total", "available"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col.capitalize())

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        tk.Button(btns, text="Add Book", command=self.open_add_book).pack(side="left", padx=5)
        tk.Button(btns, text="Delete Book", command=self.delete_book).pack(side="left", padx=5)

        self.load_books()

    def load_books(self):
        self.table.delete(*self.table.get_children())
        for b in self.controller.get_books():
            self.table.insert("", "end", iid=b[0], values=b[1:])

    def delete_book(self):
        book_id = self.table.focus()
        if not book_id:
            messagebox.showwarning("Warning", "Select a book first")
            return

        # 🔥 POPUP XÁC NHẬN
        confirm = messagebox.askyesno(
            "Confirm delete",
            "Are you sure you want to delete this book?"
        )

        if not confirm:
            return  # user bấm No → không làm gì

        self.controller.delete_book(book_id)
        messagebox.showinfo("Success", "Book deleted successfully")
        self.load_books()

    
    # add book
    def open_add_book(self):
        popup = tk.Toplevel(self)
        popup.title("Add Book")
        popup.geometry("300x420")
        popup.resizable(False, False)

        tk.Label(popup, text="Title").pack(pady=(10, 0))
        ent_title = tk.Entry(popup)
        ent_title.pack()

        tk.Label(popup, text="Author").pack(pady=(10, 0))
        ent_author = tk.Entry(popup)
        ent_author.pack()

        tk.Label(popup, text="Category").pack(pady=(10, 0))
        ent_category = tk.Entry(popup)
        ent_category.pack()

        tk.Label(popup, text="Detail").pack(pady=(10, 0))
        ent_detail = tk.Entry(popup)
        ent_detail.pack()

        tk.Label(popup, text="Total").pack(pady=(10, 0))
        ent_total = tk.Entry(popup)
        ent_total.pack()


        tk.Button(
            popup,
            text="Create",
            command=lambda: self.create_book(
                ent_title.get(),
                ent_author.get(),
                ent_category.get(),
                ent_detail.get(),
                ent_total.get(),
                popup
            )
        ).pack(pady=15)

    def create_book(self, title, author, category, detail, total, popup):
        title = title.strip()
        author = author.strip()
        category = category.strip()
        detail = detail.strip()
        total = total.strip()

        # ===== VALIDATE TOTAL =====
        if total == "":
            total = 0
        elif total.isdigit():
            total = int(total)
        else:
            messagebox.showwarning(
                "Invalid data",
                "Total copies must be a number"
            )
            return

        if total < 0:
            messagebox.showwarning(
                "Invalid data",
                "Total copies cannot be negative"
            )
            return

        # ===== CALL CONTROLLER =====
        success = self.controller.add_book(
            title,
            author,
            category,
            detail,
            total
        )

        if success:
            popup.destroy()
            self.load_books()
