"""
スキルマトリックスマネージャー UI総合テスト
Created: 2025-02-09 14:59:16
Author: GingaDza
"""

import sys
import unittest
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget,
    QComboBox, QGroupBox
)
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from unittest.mock import MagicMock, patch
from datetime import datetime

from skill_matrix_manager.views.main_window import MainWindow
from skill_matrix_manager.models.database import Database
from skill_matrix_manager.views.system_tab.system_tab import SystemTab

class TestUIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        cls.db = Database(':memory:')
        cls.main_window = MainWindow(cls.db)
        
    def setUp(self):
        self.test_data = {
            'group': {'id': 1, 'name': 'テストグループ'},
            'category': {'id': 1, 'name': 'テストカテゴリー'},
            'skill': {'id': 1, 'name': 'テストスキル', 'level': 3},
            'user': {'id': 1, 'name': 'テストユーザー'}
        }
        self.db.init_database()
    
    def test_main_window_init(self):
        """メインウィンドウの初期化テスト"""
        self.assertIsNotNone(self.main_window)
        self.assertEqual(self.main_window.windowTitle(), 'スキルマトリックスマネージャー')
    
    def test_system_tab_init(self):
        """システムタブの初期化テスト"""
        system_tab = self.main_window.findChild(SystemTab)
        self.assertIsNotNone(system_tab)
    
    def test_group_management(self):
        """グループ管理機能テスト"""
        system_tab = self.main_window.findChild(SystemTab)
        add_btn = system_tab.findChild(QPushButton, '追加')
        QTest.mouseClick(add_btn, Qt.LeftButton)
    
    def test_category_management(self):
        """カテゴリー管理機能テスト"""
        system_tab = self.main_window.findChild(SystemTab)
        category_list = system_tab.findChild(QListWidget, '親カテゴリーリスト')
        self.assertIsNotNone(category_list)
    
    def test_skill_gap_visualization(self):
        """スキルギャップ可視化機能テスト"""
        system_tab = self.main_window.findChild(SystemTab)
        radar_chart = system_tab.radar_chart
        self.assertIsNotNone(radar_chart)
    
    @classmethod
    def tearDownClass(cls):
        cls.main_window.close()
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()