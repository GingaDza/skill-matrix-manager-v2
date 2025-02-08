#!/usr/bin/env python3
"""データベース接続テスト"""
import sqlite3
from datetime import datetime

def test_database_connection(db_path="skill_matrix.db"):
    """データベース接続をテスト"""
    try:
        with sqlite3.connect(db_path) as conn:
            # 1. テーブル一覧を取得
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print("\n📊 データベーステーブル:")
            for table in tables:
                print(f"- {table[0]}")
                
            # 2. ユーザー数を確認
            cursor = conn.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"\n👥 ユーザー数: {user_count}")
            
            # 3. スキル数を確認
            cursor = conn.execute("SELECT COUNT(*) FROM skills")
            skill_count = cursor.fetchone()[0]
            print(f"🎯 スキル数: {skill_count}")
            
            # 4. ユーザースキル数を確認
            cursor = conn.execute("SELECT COUNT(*) FROM user_skills")
            user_skill_count = cursor.fetchone()[0]
            print(f"📈 ユーザースキル数: {user_skill_count}")
            
            print("\n✅ データベース接続テスト成功!")
            return True
            
    except Exception as e:
        print(f"\n❌ データベース接続エラー: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
