"""ユーザー管理機能のテスト
Created: 2025-02-08 14:17:07
Author: GingaDza
"""
import unittest
from src.database.user_manager import UserManager
from src.database.group_manager import GroupManager

class TestUserManagement(unittest.TestCase):
    """ユーザー管理機能のテスト"""

    def setUp(self):
        """テスト環境のセットアップ"""
        self.user_manager = UserManager("test_skill_matrix.db")
        self.group_manager = GroupManager("test_skill_matrix.db")
        self.group_id = self.group_manager.create_group("テストグループ")

    def test_create_user(self):
        """ユーザー作成のテスト"""
        user_id = self.user_manager.create_user("テストユーザー", self.group_id)
        self.assertIsNotNone(user_id)
        
        user = self.user_manager.get_user(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "テストユーザー")
        self.assertEqual(user.group_id, self.group_id)

    def test_update_user(self):
        """ユーザー更新のテスト"""
        user_id = self.user_manager.create_user("更新前", self.group_id)
        success = self.user_manager.update_user(user_id, "更新後", self.group_id)
        self.assertTrue(success)
        
        user = self.user_manager.get_user(user_id)
        self.assertEqual(user.name, "更新後")

    def test_delete_user(self):
        """ユーザー削除のテスト"""
        user_id = self.user_manager.create_user("削除対象", self.group_id)
        success = self.user_manager.delete_user(user_id)
        self.assertTrue(success)
        
        user = self.user_manager.get_user(user_id)
        self.assertIsNone(user)

    def tearDown(self):
        """テスト環境のクリーンアップ"""
        import os
        if os.path.exists("test_skill_matrix.db"):
            os.remove("test_skill_matrix.db")

if __name__ == '__main__':
    unittest.main()
