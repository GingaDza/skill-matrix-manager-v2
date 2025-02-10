"""評価管理モジュール
Created: 2025-02-08 20:58:32
Author: GingaDza
"""
from typing import List, Optional
from ..models.evaluation import Evaluation
from .base_manager import BaseManager

class EvaluationManager(BaseManager):
    """評価管理クラス"""

    def get_init_sql(self) -> str:
        return """
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            level INTEGER NOT NULL CHECK (level >= 1 AND level <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id),
            UNIQUE(user_id, skill_id)
        );
        """

    def set_evaluation(self, user_id: int, skill_id: int, level: int) -> bool:
        """評価を設定または更新"""
        if not 1 <= level <= 5:
            self.logger.error(f"無効なスキルレベル: {level}")
            return False
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO evaluations (user_id, skill_id, level)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, skill_id) 
                    DO UPDATE SET level = ?, updated_at = CURRENT_TIMESTAMP
                """, (user_id, skill_id, level, level))
                return True
        except Exception as e:
            self.logger.error(f"評価の設定に失敗しました: {e}")
            return False

    def get_user_evaluations(self, user_id: int) -> List[Evaluation]:
        """ユーザーの全評価を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.*, s.name as skill_name, c.name as category_name
                    FROM evaluations e
                    JOIN skills s ON e.skill_id = s.id
                    JOIN categories c ON s.category_id = c.id
                    WHERE e.user_id = ?
                """, (user_id,))
                return [Evaluation(**dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"評価の取得に失敗しました: {e}")
            return []