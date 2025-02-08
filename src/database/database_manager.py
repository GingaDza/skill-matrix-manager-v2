"""データベース管理モジュール"""
import os
import sqlite3
import logging

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path="skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path
        
        try:
            self.connection = sqlite3.connect(db_path)
            self.logger.info(f"データベース {db_path} に接続しました")
            
            # テーブルの作成
            self._create_tables()
            self.logger.debug("テーブルの作成が完了しました")
            
        except Exception as e:
            self.logger.error(f"データベース接続エラー: {e}")
            raise

    def _create_tables(self):
        """必要なテーブルを作成"""
        try:
            cursor = self.connection.cursor()
            
            # グループテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # ユーザーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    display_name TEXT,
                    email TEXT,
                    group_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            """)
            
            # カテゴリーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # スキルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            self.connection.commit()
            
        except Exception as e:
            self.logger.error(f"テーブル作成エラー: {e}")
            raise

    def close(self):
        """データベース接続を閉じる"""
        try:
            if self.connection:
                self.connection.close()
                self.logger.info("データベース接続を閉じました")
        except Exception as e:
            self.logger.error(f"データベース切断エラー: {e}")
            raise

    def get_groups(self):
        """
        全てのグループを取得
        
        Returns:
            list: グループのリスト。各グループは (id, name, description) の形式
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, name, description 
                FROM groups 
                ORDER BY name
            """)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"グループ一覧取得エラー: {e}")
            return []

    def add_group(self, name, description=""):
        """
        新しいグループを追加
        
        Args:
            name (str): グループ名
            description (str, optional): グループの説明
            
        Returns:
            int: 追加されたグループのID
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO groups (name, description)
                VALUES (?, ?)
            """, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"グループ追加エラー: {e}")
            self.connection.rollback()
            raise

    def update_group(self, group_id, name, description=""):
        """
        グループ情報を更新
        
        Args:
            group_id (int): グループID
            name (str): 新しいグループ名
            description (str, optional): 新しい説明
            
        Returns:
            bool: 更新が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE groups 
                SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, description, group_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"グループ更新エラー: {e}")
            self.connection.rollback()
            return False

    def delete_group(self, group_id):
        """
        グループを削除
        
        Args:
            group_id (int): 削除するグループのID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            # まず、このグループに属するユーザーのgroup_idをNULLに設定
            cursor.execute("""
                UPDATE users 
                SET group_id = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE group_id = ?
            """, (group_id,))
            
            # グループを削除
            cursor.execute("""
                DELETE FROM groups 
                WHERE id = ?
            """, (group_id,))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"グループ削除エラー: {e}")
            self.connection.rollback()
            return False

    def get_group_by_id(self, group_id):
        """
        指定されたIDのグループを取得
        
        Args:
            group_id (int): グループID
            
        Returns:
            tuple: (id, name, description) または None
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, name, description 
                FROM groups 
                WHERE id = ?
            """, (group_id,))
            return cursor.fetchone()
        except Exception as e:
            self.logger.error(f"グループ取得エラー: {e}")
            return None

    def get_users_in_group(self, group_id):
        """
        指定されたグループに属するユーザーを取得
        
        Args:
            group_id (int): グループID
            
        Returns:
            list: ユーザーのリスト。各ユーザーは (id, username, display_name) の形式
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, username, display_name 
                FROM users 
                WHERE group_id = ?
                ORDER BY username
            """, (group_id,))
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"グループユーザー取得エラー: {e}")
            return []

    # サンプルデータ追加用のメソッド（開発用）
    def add_sample_groups(self):
        """開発用のサンプルグループを追加"""
        try:
            sample_groups = [
                ("開発チーム", "システム開発を担当するチーム"),
                ("デザインチーム", "UIデザインを担当するチーム"),
                ("テストチーム", "品質保証を担当するチーム")
            ]
            
            cursor = self.connection.cursor()
            for name, description in sample_groups:
                try:
                    cursor.execute("""
                        INSERT INTO groups (name, description)
                        VALUES (?, ?)
                    """, (name, description))
                except sqlite3.IntegrityError:
                    # 既に存在する場合はスキップ
                    continue
                    
            self.connection.commit()
            self.logger.info("サンプルグループを追加しました")
            
        except Exception as e:
            self.logger.error(f"サンプルグループ追加エラー: {e}")
            self.connection.rollback()

    # カテゴリー関連のメソッド
    def get_categories(self):
        """
        全てのカテゴリーを取得
        
        Returns:
            list: カテゴリーのリスト。各カテゴリーは (id, name, description) の形式
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id, name, description 
                FROM categories 
                ORDER BY name
            """)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"カテゴリー一覧取得エラー: {e}")
            return []

    def add_category(self, name, description=""):
        """
        新しいカテゴリーを追加
        
        Args:
            name (str): カテゴリー名
            description (str, optional): カテゴリーの説明
            
        Returns:
            int: 追加されたカテゴリーのID
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO categories (name, description)
                VALUES (?, ?)
            """, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"カテゴリー追加エラー: {e}")
            self.connection.rollback()
            raise

    def update_category(self, category_id, name, description=""):
        """
        カテゴリー情報を更新
        
        Args:
            category_id (int): カテゴリーID
            name (str): 新しいカテゴリー名
            description (str, optional): 新しい説明
            
        Returns:
            bool: 更新が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE categories 
                SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, description, category_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー更新エラー: {e}")
            self.connection.rollback()
            return False

    def delete_category(self, category_id):
        """
        カテゴリーを削除
        
        Args:
            category_id (int): 削除するカテゴリーのID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            # このカテゴリーに属するスキルを未分類に変更
            cursor.execute("""
                UPDATE skills 
                SET category_id = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE category_id = ?
            """, (category_id,))
            
            # カテゴリーを削除
            cursor.execute("""
                DELETE FROM categories 
                WHERE id = ?
            """, (category_id,))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー削除エラー: {e}")
            self.connection.rollback()
            return False

    # スキル関連のメソッド
    def get_skills(self, category_id=None):
        """
        スキル一覧を取得
        
        Args:
            category_id (int, optional): カテゴリーIDによるフィルタリング
            
        Returns:
            list: スキルのリスト。各スキルは (id, name, description, category_id) の形式
        """
        try:
            cursor = self.connection.cursor()
            if category_id is None:
                cursor.execute("""
                    SELECT s.id, s.name, s.description, s.category_id,
                           c.name as category_name
                    FROM skills s
                    LEFT JOIN categories c ON s.category_id = c.id
                    ORDER BY c.name, s.name
                """)
            else:
                cursor.execute("""
                    SELECT s.id, s.name, s.description, s.category_id,
                           c.name as category_name
                    FROM skills s
                    LEFT JOIN categories c ON s.category_id = c.id
                    WHERE s.category_id = ?
                    ORDER BY s.name
                """, (category_id,))
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"スキル一覧取得エラー: {e}")
            return []

    def add_skill(self, name, description="", category_id=None):
        """
        新しいスキルを追加
        
        Args:
            name (str): スキル名
            description (str, optional): スキルの説明
            category_id (int, optional): カテゴリーID
            
        Returns:
            int: 追加されたスキルのID
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO skills (name, description, category_id)
                VALUES (?, ?, ?)
            """, (name, description, category_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"スキル追加エラー: {e}")
            self.connection.rollback()
            raise

    def update_skill(self, skill_id, name, description="", category_id=None):
        """
        スキル情報を更新
        
        Args:
            skill_id (int): スキルID
            name (str): 新しいスキル名
            description (str, optional): 新しい説明
            category_id (int, optional): 新しいカテゴリーID
            
        Returns:
            bool: 更新が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE skills 
                SET name = ?, description = ?, category_id = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (name, description, category_id, skill_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"スキル更新エラー: {e}")
            self.connection.rollback()
            return False

    def delete_skill(self, skill_id):
        """
        スキルを削除
        
        Args:
            skill_id (int): 削除するスキルのID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                DELETE FROM skills 
                WHERE id = ?
            """, (skill_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"スキル削除エラー: {e}")
            self.connection.rollback()
            return False

    def add_sample_categories(self):
        """開発用のサンプルカテゴリーを追加"""
        try:
            sample_categories = [
                ("プログラミング", "プログラミング言語やフレームワークに関するスキル"),
                ("データベース", "データベース設計と運用に関するスキル"),
                ("インフラ", "サーバーやネットワークに関するスキル"),
                ("プロジェクト管理", "プロジェクトマネジメントに関するスキル")
            ]
            
            cursor = self.connection.cursor()
            for name, description in sample_categories:
                try:
                    cursor.execute("""
                        INSERT INTO categories (name, description)
                        VALUES (?, ?)
                    """, (name, description))
                except sqlite3.IntegrityError:
                    continue
                    
            self.connection.commit()
            self.logger.info("サンプルカテゴリーを追加しました")
            
        except Exception as e:
            self.logger.error(f"サンプルカテゴリー追加エラー: {e}")
            self.connection.rollback()

    def add_sample_skills(self):
        """開発用のサンプルスキルを追加"""
        try:
            # カテゴリーIDを取得
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name FROM categories")
            categories = {name: id for id, name in cursor.fetchall()}
            
            sample_skills = [
                ("Python", "Pythonプログラミング", categories.get("プログラミング")),
                ("Java", "Javaプログラミング", categories.get("プログラミング")),
                ("SQL", "データベース操作", categories.get("データベース")),
                ("Docker", "コンテナ技術", categories.get("インフラ")),
                ("Git", "バージョン管理", categories.get("プログラミング")),
                ("Scrum", "アジャイル開発手法", categories.get("プロジェクト管理"))
            ]
            
            for name, description, category_id in sample_skills:
                try:
                    cursor.execute("""
                        INSERT INTO skills (name, description, category_id)
                        VALUES (?, ?, ?)
                    """, (name, description, category_id))
                except sqlite3.IntegrityError:
                    continue
                    
            self.connection.commit()
            self.logger.info("サンプルスキルを追加しました")
            
        except Exception as e:
            self.logger.error(f"サンプルスキル追加エラー: {e}")
            self.connection.rollback()
