from controllers.return_controller import return_book


def return_book_view(member_id):
    print("\n=== RETURN BOOK ===")
    book_id = input("Nhập ID sách cần trả: ")

    success, result = return_book(member_id, book_id)

    if not success:
        print("❌", result)
        return

    print("✅ Trả sách thành công")
    print(f"📅 Ngày trả: {result['return_date']}")

    if result['fine'] > 0:
        print(f"⏰ Trễ {result['overdue_days']} ngày")
        print(f"💰 Tiền phạt: {result['fine']} VND")
    else:
        print("🎉 Không có tiền phạt")
