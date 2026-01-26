"""
Login View - GUI for user authentication
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        
        # Configure root window
        self.root.title("Library Management System - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(0, 30))
        
        title_label = ttk.Label(
            header_frame,
            text="📚 Library Management System",
            font=("Arial", 20, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Welcome! Please login to continue",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Login form frame
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        username_label = ttk.Label(form_frame, text="Username:", font=("Arial", 10))
        username_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.username_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        self.username_entry.grid(row=1, column=0, pady=(0, 15))
        self.username_entry.focus()
        
        # Password
        password_label = ttk.Label(form_frame, text="Password:", font=("Arial", 10))
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.password_entry = ttk.Entry(form_frame, width=35, show="●", font=("Arial", 10))
        self.password_entry.grid(row=3, column=0, pady=(0, 5))
        
        # Show/Hide password
        self.show_password_var = tk.BooleanVar()
        show_password_check = ttk.Checkbutton(
            form_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password
        )
        show_password_check.grid(row=4, column=0, sticky=tk.W, pady=(0, 20))
        
        # Login button
        login_button = ttk.Button(
            form_frame,
            text="Login",
            command=self.handle_login,
            width=20
        )
        login_button.grid(row=5, column=0, pady=(0, 10))
        
        # Continue as Guest button
        guest_button = ttk.Button(
            form_frame,
            text="Continue as Guest",
            command=self.handle_guest_login,
            width=20
        )
        guest_button.grid(row=6, column=0)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Footer
        footer_label = ttk.Label(
            main_frame,
            text="© 2025 Library Management System",
            font=("Arial", 8)
        )
        footer_label.pack(side=tk.BOTTOM, pady=(20, 0))
        
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
            
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Input Required", "Please enter both username and password.")
            return
            
        # Authenticate user
        user = self.auth_controller.login(username, password)
        
        if user:
            messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
            
    def handle_guest_login(self):
        """Handle guest login"""
        guest_user = {
            'user_id': None,
            'username': 'guest',
            'full_name': 'Guest User',
            'role': 'Guest',
            'account_status': 'Active'
        }
        messagebox.showinfo("Guest Mode", "You are now browsing as a Guest.\nYou can view and search books only.")
        self.on_login_success(guest_user)
