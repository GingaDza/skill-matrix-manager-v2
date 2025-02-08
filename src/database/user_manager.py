"""ユーザー管理モジュール
Created: 2025-02-08 14:17:07
Author: GingaDza
"""
import sqlite3
from typing import List, Optional
from ..models.user import User
from .base_manager import BaseManager
from ..utils.logger import setup_logger

class UserManager(BaseManager):
    """ユーザー管理クラス"""

    def __init__(self, db_path: str = "data/skill_matrix.db"):
        super().__init__(db_path)
        self.logger = setup_logger(__name__)

    def create_user(self, name: str, group_id: int) -> Optional[int]:
        """ユーザーを作成

        Args:
            name (str): ユーザー名
            group_id (int): 所属グループID

        Returns:
            Optional[int]: 作成されたユーザーのID
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, group_id) VALUES (?, ?)",
                    (name, group_id)
                )
                user_id = cursor.lastrowid
                self.logger.info(f"ユーザー '{name}' (ID: {user_id}) を作成しました")
                return user_id
        except sqlite3.Error as e:
            self.logger.error(f"ユーザーの作成に失敗しました: {e}")
            return None

    def get_user(self, user_id: int) -> Optional[User]:
        """ユーザーを取得

        Args:
            user_id (int): ユーザーID

        Returns:
            Optional[User]: ユーザーオブジェクト
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return User(
                        id=row['id'],
                        name=row['name'],
                        group_id=row['group_id'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
        except sqlite3.Error as e:
            self.logger.error(f"ユーザーの取得に失敗しました: {e}")
            return None

    def get_users_by_group(self, group_id: int) -> List[User]:
        """グループに所属するユーザーを取得

        Args:
            group_id (int): グループID

        Returns:
            List[User]: ユーザーオブジェクトのリスト
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE group_id = ? ORDER BY name",
                    (group_id,)
                )
                return [
                    User(
                        id=row['id'],
                        name=row['name'],
                        group_id=row['group_id'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    for row in cursor.fetchall()
                ]
        except sqlite3.Error as e:
            self.logger.error(f"ユーザー一覧の取得に失敗しました: {e}")
            return []

    def update_user(self, user_id: int, name: str, group_id: int) -> bool:
        """ユーザーを更新

        Args:
            user_id (int): ユーザーID
            name (str): 新しいユーザー名
            group_id (int): 新しい所属グループID

        Returns:
            bool: 更新が成功したかどうか
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET name = ?, group_id = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (name, group_id, user_id)
                )
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"ユーザー '{name}' (ID: {user_id}) を更新しました")
                return success
        except sqlite3.Error as e:
            self.logger.error(f"ユーザーの更新に失敗しました: {e}")
            return False

    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除

        Args:
            user_id (int): ユーザーID

        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"ユーザー (ID: {user_id}) を削除しました")
                return success
        except sqlite3.Error as e:
            self.logger.error(f"ユーザーの削除に失敗しました: {e}")
            return False
