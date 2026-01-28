import tkinter as tk

class AdminView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(
            self,
            text="Admin Panel",
            font=("Arial", 20)
        ).pack(pady=20)

        tk.Button(
            self,
            text="Manage Books",
            width=25,
            command=self.manage_books
        ).pack(pady=5)

        tk.Button(
            self,
            text="Manage Members",
            width=25,
            command=self.manage_members
        ).pack(pady=5)

        tk.Button(
            self,
            text="Manage Borrow Records",
            width=25,
            command=self.manage_borrows
        ).pack(pady=5)

    def manage_books(self):
        from views.admin.manage_books_view import ManageBooksView
        from controllers.admin_book_controller import AdminBookController

        self.app.clear_screen()
        self.app.render_header("Manage Books")
        controller = AdminBookController()
        ManageBooksView(self.app.root, self.app, controller)\
            .pack(fill="both", expand=True)

    def manage_members(self):
        from views.admin.manage_members_view import ManageMembersView
        from controllers.admin_user_controller import AdminUserController

        self.app.clear_screen()
        self.app.render_header("Manage Members")
        controller = AdminUserController()
        ManageMembersView(self.app.root, self.app, controller)\
            .pack(fill="both", expand=True)

    def manage_borrows(self):
        from views.admin.manage_borrow_view import ManageBorrowView
        from controllers.admin_borrow_controller import AdminBorrowController

        self.app.clear_screen()
        self.app.render_header("Borrow Records")
        controller = AdminBorrowController()
        ManageBorrowView(self.app.root, controller)\
            .pack(fill="both", expand=True)
