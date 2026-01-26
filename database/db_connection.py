"""
database/db_connection.py

Simple sqlite3 wrapper providing DatabaseConnection.execute_query and execute_update
Used by models in the project.
"""
import sqlite3
import config
from typing import List, Dict, Any, Optional, Tuple

class DatabaseConnection:
    @staticmethod
    def get_connection() -> sqlite3.Connection:
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def execute_query(query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            if params is None:
                cur.execute(query)
            else:
                cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_update(query: str, params: Optional[Tuple[Any, ...]] = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE. Returns lastrowid for INSERT, otherwise 0.
        """
        conn = None
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            if params is None:
                cur.execute(query)
            else:
                cur.execute(query, params)
            conn.commit()
            return cur.lastrowid or 0
        finally:
            if conn:
                conn.close()
