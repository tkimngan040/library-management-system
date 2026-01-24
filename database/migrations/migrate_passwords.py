from database.databaseConnect.db_connect import get_connection
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def is_sha256_hash(value: str) -> bool:
    """
    Kiểm tra xem chuỗi có phải SHA256 hash không
    - độ dài phải == 64
    - chỉ chứa [0-9a-f]
    """
    if len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value.lower())

def migrate_passwords():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT UserID, PasswordHash FROM Users")
    rows = cursor.fetchall()

    migrated_count = 0
    skipped_count = 0

    for user_id, pw in rows:
        if is_sha256_hash(pw):
            skipped_count += 1
            continue

        hashed = hash_password(pw)
        cursor.execute("""
            UPDATE Users SET PasswordHash = ?
            WHERE UserID = ?
        """, (hashed, user_id))

        migrated_count += 1

    conn.commit()
    conn.close()

    print("=== PASSWORD MIGRATION DONE ===")
    print(f"Migrated: {migrated_count}")
    print(f"Skipped (already hashed): {skipped_count}")

if __name__ == "__main__":
    migrate_passwords()
