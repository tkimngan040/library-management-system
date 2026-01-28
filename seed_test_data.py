from database import get_connection
from datetime import date, timedelta
from models.user import User

def seed_data():
    conn = get_connection()
    cur = conn.cursor()

    # ======================
    # CLEAR OLD DATA
    # ======================
    cur.execute("DELETE FROM Fine")
    cur.execute("DELETE FROM BorrowRecord")
    cur.execute("DELETE FROM Book")
    cur.execute("DELETE FROM Users")

    # ======================
    # USERS
    # ======================
    users = [
        ("U001", "admin", User.hash_password("123"), "admin"),
        ("U002", "member1", User.hash_password("123"), "user"),
        ("U003", "member2", User.hash_password("123"), "user"),
        ("U004", "member3", User.hash_password("123"), "user"),
    ]

    cur.executemany(
        "INSERT INTO Users(UserID, Username, Password, Role) VALUES (?, ?, ?, ?)",
        users
    )

    # ======================
    # BOOKS
    # ======================
    books = [
        ("B001", "Clean Code", "Robert C. Martin", "IT", 5, 3),
        ("B002", "Design Patterns", "GoF", "IT", 4, 1),
        ("B003", "Python Crash Course", "Eric Matthes", "IT", 6, 6),
        ("B004", "Database System Concepts", "Silberschatz", "IT", 5, 2),
        ("B005", "The Pragmatic Programmer", "Andrew Hunt", "IT", 3, 0),
        ("B006", "To Kill a Mockingbird", "Harper Lee", "Novel", 4, 4),
        ("B007", "1984", "George Orwell", "Novel", 5, 3),
        ("B008", "Atomic Habits", "James Clear", "Self-help", 6, 5),
        ("B009", "Deep Work", "Cal Newport", "Self-help", 4, 2),
        ("B010", "Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 3, 1),
    ]

    cur.executemany(
        """
        INSERT INTO Book
        (BookID, Title, Author, Category, TotalCopies, AvailableCopies)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        books
    )

    # ======================
    # BORROW RECORDS
    # ======================
    today = date.today()

    borrows = [
        # member1 – chưa trả (chưa trễ)
        ("BR001", "U002", "B001", today - timedelta(days=2), today + timedelta(days=5), None, "Borrowed"),

        # member1 – đã trả đúng hạn
        ("BR002", "U002", "B002", today - timedelta(days=10), today - timedelta(days=3),
         today - timedelta(days=2), "Returned"),

        # member2 – trễ hạn (có fine)
        ("BR003", "U003", "B005", today - timedelta(days=15), today - timedelta(days=7),
         today - timedelta(days=1), "Returned"),

        # member3 – đang mượn
        ("BR004", "U004", "B009", today - timedelta(days=1), today + timedelta(days=6),
         None, "Borrowed"),
    ]

    cur.executemany(
        """
        INSERT INTO BorrowRecord
        (BorrowID, UserID, BookID, BorrowDate, DueDate, ReturnDate, Status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                b[0],
                b[1],
                b[2],
                b[3].isoformat(),
                b[4].isoformat(),
                b[5].isoformat() if b[5] else None,
                b[6]
            )
            for b in borrows
        ]
    )

    # ======================
    # FINE (CHO BORROW TRỄ)
    # ======================
    fines = [
        ("F001", "BR003", 30000, "Unpaid"),
    ]

    cur.executemany(
        "INSERT INTO Fine(FineID, BorrowID, Amount, Status) VALUES (?, ?, ?, ?)",
        fines
    )

    conn.commit()
    conn.close()
    print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    seed_data()
