from controllers.search_controller import SearchController
from controllers.display_controller import DisplayController
from utils.display_utils import show_books_table, paginate

class GuestView:
    """
    Đúng Interface Design - Guest chỉ được xem và tìm sách
    """

    @staticmethod
    def menu():
        while True:
            print("\n===== 📚 GUEST MENU =====")
            print("1. View all books")
            print("2. Search books")
            print("3. View book details")
            print("0. Exit")

            choice = input("Select: ")

            if choice == "1":
                GuestView.view_all_books()
            elif choice == "2":
                GuestView.search_books()
            elif choice == "3":
                GuestView.view_details()
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice")

    @staticmethod
    def view_all_books():
        books = DisplayController.get_all_books()
        page = 1
        while True:
            page_books = paginate(books, page)
            show_books_table(page_books)

            cmd = input("(N)ext, (P)rev, (E)xit: ").lower()
            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 1:
                page -= 1
            else:
                break

    @staticmethod
    def search_books():
        keyword = input("Enter title keyword: ")
        category = input("Enter category: ")

        print("\nSort by:")
        print("1. Title A-Z")
        print("2. Title Z-A")
        print("3. Availability")
        opt = input("Choose: ")

        sort_by = None
        ascending = True

        if opt == "1":
            sort_by = "title"
            ascending = True
        elif opt == "2":
            sort_by = "title"
            ascending = False
        elif opt == "3":
            sort_by = "available_copies"
            ascending = False

        results = SearchController.search_books(
            keyword=keyword if keyword else None,
            category=category if category else None,
            sort_by=sort_by,
            ascending=ascending
        )

        show_books_table(results)

    @staticmethod
    def view_details():
        book_id = input("Enter Book ID: ")
        book = DisplayController.get_book_details(book_id)

        if not book:
            print("❌ Book not found")
            return

        print("\n===== 📖 BOOK DETAILS =====")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Category: {book['category']}")
        print(f"Available: {book['available_copies']}/{book['total_copies']}")
        print(f"Description: {book['description']}")
