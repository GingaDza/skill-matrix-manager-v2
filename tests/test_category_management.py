"""カテゴリー管理機能のテスト
Created: 2025-02-08 14:19:30
Author: GingaDza
"""
import unittest
from src.database.category_manager import CategoryManager

class TestCategoryManagement(unittest.TestCase):
    """カテゴリー管理機能のテスト"""

    def setUp(self):
        """テスト環境のセットアップ"""
        self.manager = CategoryManager("test_skill_matrix.db")

    def test_create_category(self):
        """カテゴリー作成のテスト"""
        category_id = self.manager.create_category(
            "テストカテゴリー",
            description="テスト用カテゴリーです"
        )
        self.assertIsNotNone(category_id)
        
        category = self.manager.get_category(category_id)
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "テストカテゴリー")
        self.assertEqual(category.description, "テスト用カテゴリーです")

    def test_create_subcategory(self):
        """サブカテゴリー作成のテスト"""
        parent_id = self.manager.create_category("親カテゴリー")
        child_id = self.manager.create_category("子カテゴリー", parent_id=parent_id)
        
        self.assertIsNotNone(child_id)
        child = self.manager.get_category(child_id)
        self.assertEqual(child.parent_id, parent_id)

    def test_get_subcategories(self):
        """サブカテゴリー取得のテスト"""
        parent_id = self.manager.create_category("親カテゴリー")
        self.manager.create_category("子カテゴリー1", parent_id=parent_id)
        self.manager.create_category("子カテゴリー2", parent_id=parent_id)
        
        children = self.manager.get_subcategories(parent_id)
        self.assertEqual(len(children), 2)

    def tearDown(self):
        """テスト環境のクリーンアップ"""
        import os
        if os.path.exists("test_skill_matrix.db"):
            os.remove("test_skill_matrix.db")

if __name__ == '__main__':
    unittest.main()
