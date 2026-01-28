import tkinter as tk
from controllers.app_controller import AppController
from database import init_db
if __name__ == " __main__ ":
    init_db()
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("900x600")
    AppController(root)
    root.mainloop()
