"""データベース管理モジュール

Created: 2025-02-08 13:28:48
Author: GingaDza
"""
import sqlite3
import logging
from typing import List, Tuple, Optional
from ..utils.logger import setup_logger

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_name: str = "skill_matrix.db"):
        """初期化
        
        Args:
            db_name (str): データベースファイル名
        """
        self.db_name = db_name
        self.logger = setup_logger(__name__)
        self._initialize_database()
    
    def _initialize_database(self):
        """データベースの初期化"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # グループテーブル
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by TEXT DEFAULT 'GingaDza'
                    )
                ''')
                
                # カテゴリーテーブル
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by TEXT DEFAULT 'GingaDza'
                    )
                ''')
                
                # スキルテーブル
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        category_id INTEGER,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by TEXT DEFAULT 'GingaDza',
                        FOREIGN KEY (category_id) REFERENCES categories (id)
                    )
                ''')
                
                conn.commit()
                self.logger.info("データベースの初期化が完了しました")
                
        except sqlite3.Error as e:
            self.logger.error(f"データベースの初期化中にエラーが発生しました: {e}")
            raise
    
    def get_groups(self) -> List[Tuple]:
        """グループ一覧を取得
        
        Returns:
            List[Tuple]: グループのリスト [(id, name, description), ...]
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, description FROM groups")
                return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"グループ一覧の取得中にエラーが発生しました: {e}")
            return []
    
    def add_group(self, name: str, description: str = "") -> bool:
        """グループを追加
        
        Args:
            name (str): グループ名
            description (str, optional): 説明
        
        Returns:
            bool: 追加が成功したかどうか
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, description) VALUES (?, ?)",
                    (name, description)
                )
                conn.commit()
                self.logger.info(f"グループ '{name}' を追加しました")
                return True
        except sqlite3.Error as e:
            self.logger.error(f"グループの追加中にエラーが発生しました: {e}")
            return False
    
    def get_categories(self) -> List[Tuple]:
        """カテゴリー一覧を取得
        
        Returns:
            List[Tuple]: カテゴリーのリスト [(id, name, description), ...]
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, description FROM categories")
                return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"カテゴリー一覧の取得中にエラーが発生しました: {e}")
            return []
