"""
データベースマネージャー
Created: 2025-02-09 13:12:05
Author: GingaDza
"""
import sqlite3
from datetime import datetime

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path):
        """初期化"""
        self.db_path = db_path
        self.setup_database()
        self.insert_sample_data()
    
    def setup_database(self):
        """データベースのセットアップ"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # テーブルの作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_skills (
                    user_id INTEGER,
                    skill_id INTEGER,
                    level INTEGER DEFAULT 0,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (skill_id) REFERENCES skills (id),
                    PRIMARY KEY (user_id, skill_id)
                )
            ''')
            
            conn.commit()
    
    def insert_sample_data(self):
        """サンプルデータの挿入"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 既存データの確認
            cursor.execute('SELECT COUNT(*) FROM groups')
            if cursor.fetchone()[0] > 0:
                return
            
            # グループの追加
            groups = [
                ('開発チーム',),
                ('デザインチーム',),
                ('マネジメントチーム',)
            ]
            cursor.executemany(
                'INSERT INTO groups (name) VALUES (?)',
                groups
            )
            
            # ユーザーの追加
            users = [
                ('山田太郎', 1),
                ('鈴木一郎', 1),
                ('佐藤花子', 2),
                ('田中次郎', 2),
                ('高橋三郎', 3)
            ]
            cursor.executemany(
                'INSERT INTO users (name, group_id) VALUES (?, ?)',
                users
            )
            
            # スキルの追加
            skills = [
                ('Python', 'プログラミング'),
                ('JavaScript', 'プログラミング'),
                ('UI設計', 'デザイン'),
                ('UX設計', 'デザイン'),
                ('プロジェクト管理', 'マネジメント')
            ]
            cursor.executemany(
                'INSERT INTO skills (name, category) VALUES (?, ?)',
                skills
            )
            
            conn.commit()
    
    def get_groups(self):
        """グループ一覧の取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM groups ORDER BY name')
            return cursor.fetchall()
    
    def get_users_in_group(self, group_id):
        """グループ内のユーザー一覧の取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name FROM users 
                WHERE group_id = ? 
                ORDER BY name
            ''', (group_id,))
            return cursor.fetchall()

    def setup_skill_gap_table(self):
        """スキルギャップ設定テーブルの作成"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_gap_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    skill_id INTEGER,
                    target_level INTEGER,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (skill_id) REFERENCES skills (id)
                )
            ''')
            
            conn.commit()

    def save_skill_gap_settings(self, settings):
        """スキルギャップ設定の保存"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for category_id, skills in settings.items():
                for skill_id, target_level in skills.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO skill_gap_settings
                        (category_id, skill_id, target_level)
                        VALUES (?, ?, ?)
                    ''', (category_id, skill_id, target_level))
            
            conn.commit()

    def get_skill_gap_settings(self, category_id=None):
        """スキルギャップ設定の取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if category_id:
                cursor.execute('''
                    SELECT skill_id, target_level
                    FROM skill_gap_settings
                    WHERE category_id = ?
                ''', (category_id,))
            else:
                cursor.execute('''
                    SELECT skill_id, target_level
                    FROM skill_gap_settings
                ''')
            
            return dict(cursor.fetchall())
