import tkinter as tk
from views.admin_view import AdminView

class MainMenuView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Library Management System",
                 font=("Arial", 22)).pack(pady=30)

        tk.Button(
            self,
            text="Admin Panel",
            width=25,
            command=lambda: app.show_view(AdminView)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Logout",
            command=self.logout
        ).pack()

    def logout(self):
        self.app.current_user = None
        from views.login_view import LoginView
        self.app.show_view(LoginView)
