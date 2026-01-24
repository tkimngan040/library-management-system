from backend.models.user_model import User
from database.databaseConnect.db_connect import get_connection
import hashlib

# ===== SESSION =====
current_user = None

def set_current_user(user):
    global current_user
    current_user = user

def get_current_user():
    return current_user

def clear_session():
    global current_user
    current_user = None

def is_authenticated():
    return current_user is not None


# ===== HASH / DAO =====
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_username(username: str) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT UserID, Username, PasswordHash, FullName, Email, Role, Status
        FROM Users
        WHERE Username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return User(*row)
    return None

def update_password(user_id: int, new_password: str):
    hashed = hash_password(new_password)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Users
        SET PasswordHash = ?
        WHERE UserID = ?
    """, (hashed, user_id))

    conn.commit()
    conn.close()


# ===== AUTH LOGIC =====
def login():
    print("\n===== LOGIN =====")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = get_user_by_username(username)

    if not user:
        print("User does not exist.")
        return None

    db_pw = user.password_hash

    if len(db_pw) != 64:
        hashed = hash_password(db_pw)
        update_password(user.user_id, db_pw)
        user.password_hash = hashed
        db_pw = hashed

    if db_pw != hash_password(password):
        print("Incorrect password.")
        return None

    if user.status.lower() != "active":
        print("Account is blocked.")
        return None

    set_current_user(user)
    print(f"Login success! Welcome, {user.username} ({user.role})")
    return user

def logout():
    clear_session()
    print("You have been logged out.")

def change_password():
    user = get_current_user()
    if not user:
        print("You must login first.")
        return

    print("\n===== CHANGE PASSWORD =====")
    old_pw = input("Old password: ").strip()

    if user.password_hash != hash_password(old_pw):
        print("Wrong old password.")
        return

    new_pw = input("New password: ").strip()
    confirm_pw = input("Confirm new password: ").strip()

    if new_pw != confirm_pw:
        print("Password does not match.")
        return

    update_password(user.user_id, new_pw)
    print("Password updated successfully!")


# ===== AUTHORIZATION =====
def require_login():
    return get_current_user() is not None

def require_role(role: str):
    user = get_current_user()
    return user and user.role.lower() == role.lower()

def has_role(*roles):
    user = get_current_user()
    if not user:
        return False
    return user.role.lower() in [r.lower() for r in roles]
