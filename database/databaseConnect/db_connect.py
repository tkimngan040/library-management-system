import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\MSSQLSERVER01;"
            "DATABASE=LibraryManagement;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None
