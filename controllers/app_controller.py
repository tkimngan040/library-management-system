import tkinter as tk
from controllers.auth_controller import AuthController
from controllers.admin_controller import AdminController
from controllers.member_controller import MemberController
from controllers.book_controller import BookController
from controllers.history_controller import HistoryController

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_user = None

        self.auth = AuthController(self)
        self.admin = AdminController(self)
        self.member = MemberController(self)
        self.book = BookController(self)
        self.history = HistoryController(self)

        self.auth.show_login()

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

    def render_header(self, title):
        header = tk.Frame(self.root, bg="#2c3e50", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg="#2c3e50", width=120)
        center = tk.Frame(header, bg="#2c3e50")
        right = tk.Frame(header, bg="#2c3e50", width=300)

        left.pack(side="left", fill="y")
        center.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="y")

        tk.Button(
            left, text="⬅ Back", width=12,
            command=self.go_back,
            bg="#34495e", fg="white"
        ).pack(expand=True)

        tk.Label(
            center, text=title,
            bg="#2c3e50", fg="white",
            font=("Arial", 11, "bold")
        ).pack(expand=True)

        right_inner = tk.Frame(right, bg="#2c3e50")
        right_inner.pack(anchor="e", padx=10, expand=True)

        if not self.current_user:
            tk.Button(
                right_inner, text="Login", width=12,
                bg="#27ae60", fg="white",
                command=self.auth.show_login
            ).pack(side="right")
        else:
            tk.Button(
                right_inner, text="Logout", width=12,
                bg="#e74c3c", fg="white",
                command=self.auth.logout
            ).pack(side="right", padx=(5,0))

            tk.Button(
                right_inner, text="Change PW", width=12,
                bg="#2c3e50", fg="white",
                command=self.auth.show_change_password
            ).pack(side="right")

    def go_back(self):
        if not self.current_user:
            return
        if self.current_user.role.lower() == "admin":
            self.admin.show_admin_dashboard()
        else:
            self.member.show_member_dashboard()
