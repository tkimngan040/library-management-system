from models.borrow import Borrow

class AdminBorrowController:
    def __init__(self):
        self.model = Borrow()

    def get_records(self):
        return self.model.get_all()
