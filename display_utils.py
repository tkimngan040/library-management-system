from tabulate import tabulate

def show_books_table(books):
    """Hiển thị danh sách sách dạng bảng"""
    if not books:
        print("❌ Không có sách nào.")
        return

    headers = ["Book ID", "Title", "Author", "Category", "Status"]
    table = []

    for b in books:
        status = "Available" if b["available_copies"] > 0 else "Borrowed"
        table.append([
            b["book_id"],
            b["title"],
            b["author"],
            b["category"],
            status
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))


def paginate(data, page, limit=5):
    start = (page - 1) * limit
    end = start + limit
    return data[start:end]
