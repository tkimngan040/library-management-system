from controllers.auth_controller import login, logout, change_password, get_current_user
user = login()

if user:
    print("Current user:", get_current_user())
    change_password()
    logout()
