"""グループ管理クラス
Created: 2025-02-08 20:44:07
Author: GingaDza
"""
from typing import List, Optional
from .base_manager import BaseManager
from ..models.group import Group

class GroupManager(BaseManager):
    """グループ管理クラス"""

    def get_init_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

    def create_group(self, name: str, description: str = "") -> Optional[int]:
        """グループの作成"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, description) VALUES (?, ?)",
                    (name, description)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"グループの作成に失敗しました: {e}")
            return None

    def get_all_groups(self) -> List[Group]:
        """全グループの取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM groups ORDER BY name")
                return [
                    Group(
                        id=row['id'],
                        name=row['name'],
                        description=row['description'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            self.logger.error(f"グループ一覧の取得に失敗しました: {e}")
            return []
