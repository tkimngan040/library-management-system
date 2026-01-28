import tkinter as tk

class MemberView(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller  # MemberController

        tk.Label(
            self,
            text="MEMBER DASHBOARD",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        tk.Button(
            self,
            text="📚 View Book List",
            width=30,
            height=2,
            command=self.controller.app.book.show_books
        ).pack(pady=10)

        tk.Button(
            self,
            text="📜 Borrow History",
            width=30,
            height=2,
            command=self.controller.app.history.show_history
        ).pack(pady=10)
