import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "library.db")

# Business settings
BORROW_PERIOD_DAYS = 14
MAX_BOOKS_PER_MEMBER = 5
FINE_PER_DAY = 10000  # VND per day

# Account statuses
ACCOUNT_LOCKED = "Locked"
