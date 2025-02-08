"""データベース接続テスト
Created: 2025-02-08 14:09:30
Author: GingaDza
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def test_connection():
    """データベース接続テスト"""
    db = DatabaseManager()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info("既存のテーブル:")
        for table in tables:
            logger.info(f"- {table[0]}")

if __name__ == "__main__":
    test_connection()
