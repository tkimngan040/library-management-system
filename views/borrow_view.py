# views/borrow_view.py
from controllers.borrow_controller import borrow_book

def borrow_book_interface(user_id):
    print("\n===== MƯỢN SÁCH =====")

    # Nhập ID sách cần mượn
    book_id = input("Nhập ID sách cần mượn: ")

    # Gọi hàm mượn sách
    success, message = borrow_book(user_id, book_id)

    # Hiển thị kết quả
    if success:
        print("✅", message)
    else:
        print("❌", message)
