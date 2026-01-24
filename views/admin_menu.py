from controllers.auth_controller import login, logout, get_current_user, is_authenticated, has_role

def admin_menu():
    print("\n=== ADMIN MENU ===")
    print("1. Manage Users")
    print("2. Manage Books")
    print("3. Logout")
    logout()
    return

