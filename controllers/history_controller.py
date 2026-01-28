from models.borrow import Borrow
from views.history_view import HistoryView

class HistoryController:
    def __init__(self, app):
        self.app = app

    # màn lịch sử mượn sách
    def show_history(self):
        self.app.clear_screen()
        self.app.render_header("Borrow History")
        borrows = Borrow.get_by_user(self.app.current_user.id)
        HistoryView(self.app.root, self, borrows).pack(fill="both", expand=True)
