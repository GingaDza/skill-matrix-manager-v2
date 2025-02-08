"""グループ管理機能のテスト
Created: 2025-02-08 14:10:30
Author: GingaDza
"""
import unittest
from src.database.group_manager import GroupManager

class TestGroupManagement(unittest.TestCase):
    """グループ管理機能のテスト"""

    def setUp(self):
        """テスト環境のセットアップ"""
        self.manager = GroupManager("test_skill_matrix.db")

    def test_create_group(self):
        """グループ作成のテスト"""
        group_id = self.manager.create_group("テストグループ", "テスト用グループです")
        self.assertIsNotNone(group_id)
        
        group = self.manager.get_group(group_id)
        self.assertIsNotNone(group)
        self.assertEqual(group.name, "テストグループ")
        self.assertEqual(group.description, "テスト用グループです")

    def test_update_group(self):
        """グループ更新のテスト"""
        group_id = self.manager.create_group("更新前", "説明文")
        success = self.manager.update_group(group_id, "更新後", "新しい説明文")
        self.assertTrue(success)
        
        group = self.manager.get_group(group_id)
        self.assertEqual(group.name, "更新後")
        self.assertEqual(group.description, "新しい説明文")

    def test_delete_group(self):
        """グループ削除のテスト"""
        group_id = self.manager.create_group("削除対象", "")
        success = self.manager.delete_group(group_id)
        self.assertTrue(success)
        
        group = self.manager.get_group(group_id)
        self.assertIsNone(group)

    def tearDown(self):
        """テスト環境のクリーンアップ"""
        import os
        if os.path.exists("test_skill_matrix.db"):
            os.remove("test_skill_matrix.db")

if __name__ == '__main__':
    unittest.main()
