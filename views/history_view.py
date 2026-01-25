from controllers.history_controller import view_borrow_history
from tabulate import tabulate


def history_view(member_id):
    records = view_borrow_history(member_id)

    if not records:
        print("📭 Chưa có lịch sử mượn sách.")
        return

    headers = ["Title", "Borrow Date", "Due Date", "Return Date", "Status", "Fine"]
    print("\n=== BORROW HISTORY ===")
    print(tabulate(records, headers=headers, tablefmt="grid"))
