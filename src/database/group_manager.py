"""グループ管理モジュール
Created: 2025-02-08 22:13:49
Author: GingaDza
"""
from typing import List, Optional
from ..models.group import Group
from .base_manager import BaseManager

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
        """グループを作成"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, description) VALUES (?, ?)",
                    (name, description)
                )
                group_id = cursor.lastrowid
                self.logger.info(f"グループ '{name}' (ID: {group_id}) を作成しました")
                return group_id
        except Exception as e:
            self.logger.error(f"グループの作成に失敗しました: {e}")
            return None

    def get_all_groups(self) -> List[Group]:
        """全グループを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM groups ORDER BY name")
                return [Group(**dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"グループ一覧の取得に失敗しました: {e}")
            return []