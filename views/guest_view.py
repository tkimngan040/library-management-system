import tkinter as tk
from tkinter import ttk
from controllers.search_controller import SearchController
from controllers.display_controller import DisplayController

class GuestView:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.parent, text="Guest Book Browser", 
                font=('Arial', 18, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        search_frame = tk.Frame(self.parent, bg='white', relief='raised', bd=1)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10)).pack(side='left', padx=10)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=40)
        self.search_entry.pack(side='left', padx=5, pady=10)
        
        tk.Button(search_frame, text="Search", bg='#3498db', fg='white',
                 command=self.search_books).pack(side='left', padx=5)
