"""
Main GUI Application Entry Point
Library Management System
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.login_view import LoginView
from views.main_menu_view import MainMenuView
from database.init_db import initialize_database

class LibraryManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide root initially
        
        # Set theme
        try:
            style = ttk.Style()
            style.theme_use('clam')  # Modern theme
        except:
            pass
            
        # Current user
        self.current_user = None
        
        # Initialize database
        print("Initializing database...")
        initialize_database()
        print("Database initialized successfully!")
        
        # Show login
        self.show_login()
        
    def show_login(self):
        """Show login window"""
        # Create new window for login
        login_window = tk.Toplevel(self.root)
        LoginView(login_window, self.on_login_success)
        
        # Handle window close
        login_window.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    def on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        
        # Close all windows except root
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
                
        # Show main menu
        self.show_main_menu()
        
    def show_main_menu(self):
        """Show main menu"""
        # Create new window for main menu
        menu_window = tk.Toplevel(self.root)
        MainMenuView(menu_window, self.current_user, self.on_logout)
        
        # Handle window close
        menu_window.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    def on_logout(self):
        """Handle logout"""
        self.current_user = None
        
        # Close all windows except root
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
                
        # Show login again
        self.show_login()
        
    def quit_app(self):
        """Quit application"""
        self.root.quit()
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("="*60)
    print("Library Management System - GUI Version")
    print("="*60)
    print()
    
    app = LibraryManagementApp()
    app.run()

if __name__ == "__main__":
    main()
