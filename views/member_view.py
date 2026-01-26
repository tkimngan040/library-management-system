from controllers.auth_controller import login, logout, get_current_user, is_authenticated, has_role

def member_view():
    print("\n=== MEMBER MENU ===")
    print("1. Borrow Book")
    print("2. History")
    print("3. Logout")
    logout()
    return