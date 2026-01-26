"""
Change Password View - Change user password
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class ChangePasswordView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.auth_controller = AuthController()
        
        # Configure window
        self.root.title("Change Password")
        self.root.geometry("450x400")
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
        title_label = ttk.Label(
            main_frame,
            text="🔐 Change Password",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Info
        info_label = ttk.Label(
            main_frame,
            text=f"User: {self.user['username']}",
            font=("Arial", 10)
        )
        info_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Old password
        ttk.Label(form_frame, text="Current Password:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.old_password_entry = ttk.Entry(form_frame, width=35, show="●", font=("Arial", 10))
        self.old_password_entry.grid(row=1, column=0, pady=(0, 15))
        self.old_password_entry.focus()
        
        # New password
        ttk.Label(form_frame, text="New Password:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.new_password_entry = ttk.Entry(form_frame, width=35, show="●", font=("Arial", 10))
        self.new_password_entry.grid(row=3, column=0, pady=(0, 15))
        
        # Confirm password
        ttk.Label(form_frame, text="Confirm New Password:", font=("Arial", 10)).grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.confirm_password_entry = ttk.Entry(form_frame, width=35, show="●", font=("Arial", 10))
        self.confirm_password_entry.grid(row=5, column=0, pady=(0, 5))
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = ttk.Checkbutton(
            form_frame,
            text="Show passwords",
            variable=self.show_password_var,
            command=self.toggle_password
        )
        show_password_check.grid(row=6, column=0, sticky=tk.W, pady=(0, 20))
        
        # Password requirements
        requirements_frame = ttk.LabelFrame(form_frame, text="Password Requirements", padding="10")
        requirements_frame.grid(row=7, column=0, sticky=tk.W+tk.E, pady=(0, 20))
        
        requirements = [
            "• At least 6 characters long",
            "• Not the same as current password"
        ]
        
        for req in requirements:
            ttk.Label(requirements_frame, text=req, font=("Arial", 9)).pack(anchor=tk.W)
            
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=8, column=0, pady=(0, 0))
        
        ttk.Button(
            button_frame,
            text="Change Password",
            command=self.change_password,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.root.destroy,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.old_password_entry.bind('<Return>', lambda e: self.new_password_entry.focus())
        self.new_password_entry.bind('<Return>', lambda e: self.confirm_password_entry.focus())
        self.confirm_password_entry.bind('<Return>', lambda e: self.change_password())
        
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.old_password_entry.config(show="")
            self.new_password_entry.config(show="")
            self.confirm_password_entry.config(show="")
        else:
            self.old_password_entry.config(show="●")
            self.new_password_entry.config(show="●")
            self.confirm_password_entry.config(show="●")
            
    def change_password(self):
        """Handle password change"""
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Validation
        if not old_password or not new_password or not confirm_password:
            messagebox.showwarning("Input Required", "Please fill all fields.")
            return
            
        if len(new_password) < 6:
            messagebox.showwarning("Weak Password", "Password must be at least 6 characters long.")
            return
            
        if new_password != confirm_password:
            messagebox.showerror("Password Mismatch", "New password and confirmation do not match.")
            self.confirm_password_entry.delete(0, tk.END)
            self.confirm_password_entry.focus()
            return
            
        if old_password == new_password:
            messagebox.showwarning("Same Password", "New password cannot be the same as current password.")
            return
            
        # Change password
        success, message = self.auth_controller.change_password(
            self.user['user_id'],
            old_password,
            new_password
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.root.destroy()
        else:
            messagebox.showerror("Error", message)
            self.old_password_entry.delete(0, tk.END)
            self.old_password_entry.focus()
