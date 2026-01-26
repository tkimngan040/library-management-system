from controllers.auth_controller import login, logout, get_current_user, is_authenticated, has_role
from views.admin_view import AdminView
# from views.member_view import MemberView
from views.guest_view import GuestView

def main():
    admin_view = AdminView()
    # member_view = MemberView()
    guest_view = GuestView()

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
                print("Invalid choice!")
                continue

        else:
            user = get_current_user()
            print(f"\nLogged in as: {user.username} ({user.role})")

            # Hiển thị menu theo role
            if has_role("admin"):
                admin_view.admin_menu()
            # elif has_role("member"):
            #     member_view.show_menu()
            else:
                guest_view.show_menu()

            # Sau khi xử lý menu thì loop trở lại

if __name__ == "__main__":
    main()
