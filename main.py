from controllers.auth_controller import login, logout, get_current_user, is_authenticated, has_role
from views.admin_menu import admin_menu
from views.guest_menu import guest_menu
from views.member_menu import member_menu

def main():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")

        if not is_authenticated():
            print("1. Login")
            print("2. Exit")
            choice = input("Choose: ").strip()

            if choice == "1":
                login()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

        else:
            user = get_current_user()
            print(f"\nLogged in as: {user.username} ({user.role})")

            # Điều hướng menu theo role
            if has_role("admin"):
                admin_menu()
            else:
                member_menu()

            # Sau khi vào menu thì tiếp tục vòng loop


if __name__ == "__main__":
    main()
