from tkinter import messagebox
from models.user import User
from views.login_view import LoginView
from views.change_password_view import ChangePasswordView

class AuthController:
    def __init__(self, app):
        self.app = app

    def show_login(self):
        self.app.current_user = None
        self.app.clear_screen()
        self.app.render_header("Login")
        LoginView(self.app.root, self).pack(expand=True)

    def handle_login(self, username, password):
        user = User.login(username, password)
        if not user:
            messagebox.showerror("Error", "Invalid login")
            return
        self.app.current_user = user
        if user.role.lower() == "admin":
            self.app.admin.show_admin_dashboard()
        else:
            self.app.member.show_member_dashboard()

    def logout(self):
        self.app.current_user = None
        self.app.book.show_books()

    def show_change_password(self):
        self.app.clear_screen()
        self.app.render_header("Change Password")
        ChangePasswordView(self.app.root, self).pack(expand=True)

    def update_password(self, old_pw, new_pw):
        from models.user import User
        current_hash = User.get_password_hash(self.app.current_user.id)
        if not User.check_password(old_pw, current_hash):
            messagebox.showerror("Error", "Old password incorrect")
            return
        User.change_password(self.app.current_user.id, new_pw)
        messagebox.showinfo("Success", "Password updated")
        self.app.member.show_member_dashboard()
    def continue_as_guest(self):
        """ Vào hệ thống với tư cách Guest """
        self.app.current_user = None
        self.app.book.show_books()

