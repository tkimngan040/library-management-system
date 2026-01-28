import tkinter as tk
from tkinter import messagebox

class ChangePasswordView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        card = tk.Frame(self, padx=40, pady=30)
        card.pack(expand=True)

        tk.Label(card, text="Change Password", font=("Arial",16,"bold")).pack(pady=10)

        tk.Label(card, text="Old Password").pack(anchor="w")
        self.old = tk.Entry(card, show="*")
        self.old.pack()

        tk.Label(card, text="New Password").pack(anchor="w")
        self.new = tk.Entry(card, show="*")
        self.new.pack()

        tk.Label(card, text="Confirm Password").pack(anchor="w")
        self.confirm = tk.Entry(card, show="*")
        self.confirm.pack()

        tk.Button(
            card, text="Update", width=25,
            command=self.submit
        ).pack(pady=15)

    def submit(self):
        if self.new.get() != self.confirm.get():
            messagebox.showerror("Error", "Passwords do not match")
            return
        self.controller.update_password(self.old.get(), self.new.get())
