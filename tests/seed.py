#!/usr/bin/env python3
"""テストデータ投入スクリプト"""
import os
import sys
import sqlite3
from datetime import datetime

def seed_database(db_path="skill_matrix.db"):
    """基本データを投入"""
    print("🌱 テストデータを投入中...")
    
    with sqlite3.connect(db_path) as conn:
        # 1. 基本ユーザーの作成
        conn.executemany(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            [
                ("admin", "admin@example.com"),
                ("manager", "manager@example.com"),
                ("user1", "user1@example.com"),
                ("user2", "user2@example.com"),
            ]
        )
        print("✓ ユーザーを作成しました")

        # 2. グループの作成
        conn.executemany(
            "INSERT INTO groups (name, description) VALUES (?, ?)",
            [
                ("開発", "開発関連スキル"),
                ("インフラ", "インフラ関連スキル"),
                ("ビジネス", "ビジネス関連スキル"),
            ]
        )
        print("✓ グループを作成しました")

        # 3. カテゴリーの作成
        conn.executemany(
            """INSERT INTO categories 
               (name, description, group_id, parent_id, display_order) 
               VALUES (?, ?, ?, ?, ?)""",
            [
                # 開発カテゴリー
                ("プログラミング言語", "各種プログラミング言語", 1, None, 1),
                ("フレームワーク", "各種フレームワーク", 1, None, 2),
                ("Python", "Pythonプログラミング", 1, 1, 1),
                ("JavaScript", "JavaScriptプログラミング", 1, 1, 2),
                
                # インフラカテゴリー
                ("クラウド", "クラウドサービス", 2, None, 1),
                ("ネットワーク", "ネットワーク技術", 2, None, 2),
                ("AWS", "Amazon Web Services", 2, 5, 1),
                ("Azure", "Microsoft Azure", 2, 5, 2),
                
                # ビジネスカテゴリー
                ("マネジメント", "マネジメントスキル", 3, None, 1),
                ("コミュニケーション", "コミュニケーションスキル", 3, None, 2),
            ]
        )
        print("✓ カテゴリーを作成しました")

        # 4. スキルの作成
        conn.executemany(
            """INSERT INTO skills 
               (name, description, category_id, min_level, max_level) 
               VALUES (?, ?, ?, ?, ?)""",
            [
                # Pythonスキル
                ("Python基礎", "Python言語の基礎知識", 3, 1, 5),
                ("Django", "Djangoフレームワーク", 3, 1, 5),
                ("FastAPI", "FastAPIフレームワーク", 3, 1, 5),
                
                # JavaScriptスキル
                ("JavaScript基礎", "JavaScript言語の基礎知識", 4, 1, 5),
                ("React", "Reactフレームワーク", 4, 1, 5),
                ("Vue.js", "Vue.jsフレームワーク", 4, 1, 5),
                
                # AWSスキル
                ("AWS EC2", "EC2の運用管理", 7, 1, 5),
                ("AWS Lambda", "Lambdaの開発と運用", 7, 1, 5),
                
                # Azureスキル
                ("Azure VM", "Azure仮想マシンの運用", 8, 1, 5),
                ("Azure Functions", "Azure Functionsの開発", 8, 1, 5),
                
                # マネジメントスキル
                ("プロジェクト管理", "プロジェクトの管理と運営", 9, 1, 5),
                ("チームリーダーシップ", "チームのリーダーシップ", 9, 1, 5),
                
                # コミュニケーションスキル
                ("ビジネス文書", "ビジネス文書の作成", 10, 1, 5),
                ("プレゼンテーション", "プレゼンテーションスキル", 10, 1, 5),
            ]
        )
        print("✓ スキルを作成しました")

        # 5. ユーザーロールの割り当て
        conn.executemany(
            "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)",
            [
                (1, 1),  # admin -> admin
                (2, 2),  # manager -> manager
                (3, 3),  # user1 -> user
                (4, 3),  # user2 -> user
            ]
        )
        print("✓ ユーザーロールを割り当てました")

        # 6. ユーザースキルの設定
        conn.executemany(
            "INSERT INTO user_skills (user_id, skill_id, level) VALUES (?, ?, ?)",
            [
                # adminのスキル
                (1, 1, 5),  # Python基礎
                (1, 2, 4),  # Django
                (1, 7, 4),  # AWS EC2
                
                # managerのスキル
                (2, 11, 5),  # プロジェクト管理
                (2, 12, 4),  # チームリーダーシップ
                (2, 14, 4),  # プレゼンテーション
                
                # user1のスキル
                (3, 1, 3),  # Python基礎
                (3, 4, 3),  # JavaScript基礎
                (3, 5, 2),  # React
                
                # user2のスキル
                (4, 7, 3),  # AWS EC2
                (4, 8, 2),  # AWS Lambda
                (4, 13, 3),  # ビジネス文書
            ]
        )
        print("✓ ユーザースキルを設定しました")

        conn.commit()
        print("\n✨ テストデータの投入が完了しました！")

def main():
    try:
        seed_database()
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
