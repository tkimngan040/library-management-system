import sqlite3
import config

class DatabaseConnection:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def execute_query(query, params=()):
        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def execute_update(query, params=()):
        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        lastrowid = cur.lastrowid
        conn.close()
        return lastrowid
