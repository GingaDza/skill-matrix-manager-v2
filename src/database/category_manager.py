"""カテゴリー管理モジュール
Created: 2025-02-08 20:58:32
Author: GingaDza
"""
from typing import List, Optional
from ..models.category import Category
from .base_manager import BaseManager

class CategoryManager(BaseManager):
    """カテゴリー管理クラス"""

    def get_init_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
        );
        """

    def create_category(self, name: str, parent_id: Optional[int] = None) -> Optional[int]:
        """カテゴリーを作成"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
                    (name, parent_id)
                )
                category_id = cursor.lastrowid
                self.logger.info(f"カテゴリー '{name}' (ID: {category_id}) を作成しました")
                return category_id
        except Exception as e:
            self.logger.error(f"カテゴリーの作成に失敗しました: {e}")
            return None

    def get_categories(self, parent_id: Optional[int] = None) -> List[Category]:
        """カテゴリー一覧を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if parent_id is None:
                    cursor.execute("SELECT * FROM categories WHERE parent_id IS NULL")
                else:
                    cursor.execute("SELECT * FROM categories WHERE parent_id = ?", (parent_id,))
                return [Category(**dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"カテゴリー一覧の取得に失敗しました: {e}")
            return []