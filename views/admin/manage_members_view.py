import tkinter as tk
from tkinter import ttk, messagebox

class ManageMembersView(tk.Frame):
    def __init__(self, parent, app, controller):
        super().__init__(parent)
        self.app = app
        self.controller = controller

        self.table = ttk.Treeview(
            self,
            columns=("username", "role"),
            show="headings"
        )
        self.table.heading("username", text="Username")
        self.table.heading("role", text="Role")
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        tk.Button(btns, text="Add User",
                  command=self.open_add_user).pack(side="left", padx=5)

        tk.Button(btns, text="Delete User",
                  command=self.delete_user).pack(side="left", padx=5)

        self.load_users()

    def load_users(self):
        self.table.delete(*self.table.get_children())
        for u in self.controller.get_users():
            self.table.insert("", "end", iid=u[0], values=u[1:])

    def delete_user(self):
        user_id = self.table.focus()
        if not user_id:
            messagebox.showwarning("Warning", "Select a user first")
            return

        confirm = messagebox.askyesno(
            "Confirm delete",
            "Are you sure you want to delete this user?"
        )

        if not confirm:
            return

        self.controller.delete_user(user_id)
        messagebox.showinfo("Success", "User deleted successfully")
        self.load_users()

    # ===== ADD USER =====
    def open_add_user(self):
        popup = tk.Toplevel(self)
        popup.title("Add User")
        popup.geometry("300x220")
        popup.resizable(False, False)

        tk.Label(popup, text="Username").pack(pady=(10, 0))
        ent_user = tk.Entry(popup)
        ent_user.pack()

        tk.Label(popup, text="Password").pack(pady=(10, 0))
        ent_pass = tk.Entry(popup, show="*")
        ent_pass.pack()

        tk.Label(popup, text="Role").pack(pady=(10, 0))
        role_var = tk.StringVar(value="user")
        ttk.Combobox(
            popup,
            textvariable=role_var,
            values=["user", "admin"],
            state="readonly"
        ).pack()

        tk.Button(
            popup,
            text="Create",
            command=lambda: self.create_user(
                ent_user.get(),
                ent_pass.get(),
                role_var.get(),
                popup
            )
        ).pack(pady=15)

    def create_user(self, username, password, role, popup):
        if self.controller.add_user(username, password, role):
            popup.destroy()
            self.load_users()

