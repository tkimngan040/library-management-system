import unittest
from controllers.borrow_controller import borrow_book

class TestBorrow(unittest.TestCase):

    def test_borrow_success(self):
        success, message = borrow_book(user_id=1, book_id=1)
        self.assertTrue(success)

    def test_borrow_fail(self):
        success, message = borrow_book(user_id=1, book_id=999)
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
