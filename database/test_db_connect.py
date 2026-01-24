from databaseConnect.db_connect import get_connection

def test_connection():
    conn = get_connection()
    if conn:
        print("Successfully connected to SQL Server!")
        conn.close()
    else:
        print("Failed to connect to SQL Server!")

if __name__ == "__main__":
    test_connection()
