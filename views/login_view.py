import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        card = tk.Frame(self, padx=40, pady=30)
        card.pack(expand=True)

        tk.Label(card, text="LIBRARY SYSTEM", font=("Arial",16,"bold")).pack(pady=10)

        tk.Label(card, text="Username").pack(anchor="w")
        self.username = tk.Entry(card, width=30)
        self.username.pack()

        tk.Label(card, text="Password").pack(anchor="w")
        self.password = tk.Entry(card, show="*", width=30)
        self.password.pack()

        tk.Button(
            card, text="Login", width=25,
            command=lambda: self.controller.handle_login(
                self.username.get(), self.password.get()
            )
        ).pack(pady=15)
        tk.Button(
            card, text="Continue as Guest", width=25, fg="#555",
            command=self.controller.continue_as_guest
        ).pack(pady=15)
