import tkinter as tk
from tkinter import ttk

class ManageBorrowView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.table = ttk.Treeview(
            self,
            columns=("user", "book", "date", "status"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col.capitalize())

        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_data()

    def load_data(self):
        self.table.delete(*self.table.get_children())
        for r in self.controller.get_records():
            self.table.insert("", "end", values=r[1:])
