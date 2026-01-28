import bcrypt
import uuid
from database import get_connection

class User:
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def login(username, password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT UserID, Username, Password, Role FROM Users WHERE Username=?",
            (username,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        if not User.check_password(password, row[2]):
            return None

        return User(row[0], row[1], row[3])

    @staticmethod
    def get_password_hash(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Password FROM Users WHERE UserID=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return row[0]

    @staticmethod
    def change_password(user_id, new_password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Users SET Password=? WHERE UserID=?",
            (User.hash_password(new_password), user_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT UserID, Username, Role FROM Users")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def create(username, password, role):
        conn = get_connection()
        cur = conn.cursor()

        password_hash = User.hash_password(password)

        cur.execute("""
            INSERT INTO Users (UserID, Username, Password, Role)
            VALUES (?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            username,
            password_hash,
            role
        ))

        conn.commit()
        conn.close()