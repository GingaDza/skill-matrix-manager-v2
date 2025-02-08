"""マイグレーション管理
Created: 2025-02-08 14:07:30
Author: GingaDza
"""
import os
import sqlite3
from typing import List, Tuple
from ...utils.logger import setup_logger

class MigrationManager:
    """マイグレーション管理クラス"""
    
    def __init__(self, db_path: str):
        self.logger = setup_logger(__name__)
        self.db_path = db_path
        self._init_migrations_table()
    
    def _init_migrations_table(self):
        """マイグレーションテーブルの初期化"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
    
    def get_applied_migrations(self) -> List[str]:
        """適用済みマイグレーションの取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM migrations ORDER BY id")
            return [row[0] for row in cursor.fetchall()]
    
    def apply_migration(self, version: str, upgrade_func) -> bool:
        """マイグレーションの適用"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                upgrade_func(cursor)
                cursor.execute(
                    "INSERT INTO migrations (version) VALUES (?)",
                    (version,)
                )
                conn.commit()
                self.logger.info(f"マイグレーション {version} を適用しました")
                return True
        except Exception as e:
            self.logger.error(f"マイグレーション {version} の適用に失敗しました: {e}")
            return False
