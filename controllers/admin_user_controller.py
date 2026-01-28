from models.user import User
from tkinter import messagebox

class AdminUserController:
    def __init__(self):
        pass

    def get_users(self):
        return User.get_all()

    def delete_user(self, user_id):
        User.delete(user_id)

    def add_user(self, username, password, role):
            if not username or not password:
                messagebox.showwarning(
                    "Invalid data",
                    "Username and password are required"
                )
                return False

            if role not in ("admin", "user"):
                messagebox.showwarning(
                    "Invalid role",
                    "Role must be admin or user"
                )
                return False

            User.create(username, password, role)
            messagebox.showinfo("Success", "User added successfully")
            return True
