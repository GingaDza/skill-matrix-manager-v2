"""
SystemTabのUIテスト
Created: 2025-02-09 14:59:16
Author: GingaDza
"""

import sys
import unittest
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QListWidget,
    QComboBox, QGroupBox
)
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from unittest.mock import MagicMock, patch
from skill_matrix_manager.views.system_tab.system_tab import SystemTab

class TestSystemTab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        self.mock_db = MagicMock()
        self.system_tab = SystemTab(self.mock_db)
    
    def test_init_tab_creation(self):
        """初期設定タブの作成テスト"""
        init_tab = self.system_tab.create_init_tab()
        self.assertIsNotNone(init_tab)
        
        group_box = init_tab.findChild(QGroupBox, '初期設定')
        self.assertIsNotNone(group_box)
    
    def test_gap_tab_creation(self):
        """スキルギャップタブの作成テスト"""
        gap_tab = self.system_tab.create_gap_tab()
        self.assertIsNotNone(gap_tab)
        
        radar_chart = self.system_tab.radar_chart
        self.assertIsNotNone(radar_chart)
    
    def test_io_tab_creation(self):
        """データ入出力タブの作成テスト"""
        io_tab = self.system_tab.create_io_tab()
        self.assertIsNotNone(io_tab)
    
    def test_info_tab_creation(self):
        """システム情報タブの作成テスト"""
        info_tab = self.system_tab.create_info_tab()
        self.assertIsNotNone(info_tab)

if __name__ == '__main__':
    unittest.main()