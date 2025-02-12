"""
メインウィンドウの実装（オリジナルUI完全コピー）
Created: 2025-02-12 13:12:20
Author: GingaDza
"""

import logging
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QMessageBox,
    QWidget, QHBoxLayout, QVBoxLayout,
    QComboBox, QListWidget, QPushButton,
    QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .styles import STYLE_SHEET

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        logger.debug("Initializing MainWindow")
        self.custom_tabs = []
        self.setupUi()

    def setupUi(self):
        # ウィンドウ設定
        self.setWindowTitle("スキルマトリックスマネージャー")
        self.setFixedSize(1280, 800)
        self.setStyleSheet(STYLE_SHEET)

        # メインウィジェット
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左ペイン (3:7の比率で)
        left_pane = self._create_left_pane()
        main_layout.addWidget(left_pane, 3)

        # 右ペイン
        right_pane = self._create_right_pane()
        main_layout.addWidget(right_pane, 7)

    def _create_left_pane(self):
        container = QFrame()
        container.setObjectName("leftPane")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # グループ選択
        group_frame = QFrame()
        group_layout = QVBoxLayout(group_frame)
        group_layout.setContentsMargins(0, 0, 0, 0)
        
        group_label = QLabel("グループ選択")
        self.group_combo = QComboBox()
        
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)

        # ユーザーリスト
        user_frame = QFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(0, 0, 0, 0)
        
        user_label = QLabel("ユーザー一覧")
        self.user_list = QListWidget()
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_list)

        # ボタン
        button_frame = QFrame()
        button_layout = QVBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        self.add_button = QPushButton("追加")
        self.add_button.setObjectName("add_button")
        
        self.edit_button = QPushButton("編集")
        self.edit_button.setObjectName("edit_button")
        
        self.delete_button = QPushButton("削除")
        self.delete_button.setObjectName("delete_button")

        for btn in [self.add_button, self.edit_button, self.delete_button]:
            button_layout.addWidget(btn)

        # レイアウトに追加
        layout.addWidget(group_frame)
        layout.addWidget(user_frame, 1)
        layout.addWidget(button_frame)

        return container

    def _create_right_pane(self):
        container = QFrame()
        container.setObjectName("rightPane")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)

        try:
            # 既存のカテゴリータブ
            for tab in self.custom_tabs:
                self.tab_widget.addTab(tab, tab.category_name)

            # 総合評価タブ
            from .evaluation_tab import EvaluationTab
            self.evaluation_tab = EvaluationTab(self.db_manager)
            self.tab_widget.addTab(self.evaluation_tab, "総合評価")

            # システム管理タブ
            from .admin.admin_tab import AdminTab
            self.admin_tab = AdminTab(self.db_manager)
            self.tab_widget.addTab(self.admin_tab, "システム管理")

            logger.debug("All tabs added successfully")
        except Exception as e:
            logger.error(f"Failed to create tabs: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー",
                f"タブの作成に失敗しました:\n{str(e)}")

        layout.addWidget(self.tab_widget)
        return container

    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        try:
            from .category_tab import CategoryTab
            new_tab = CategoryTab(self.db_manager, category_name)
            self.tab_widget.insertTab(len(self.custom_tabs), new_tab, category_name)
            self.custom_tabs.append(new_tab)
            logger.debug(f"Added new category tab: {category_name}")
        except Exception as e:
            logger.error(f"Failed to create category tab: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー",
                f"カテゴリータブの作成に失敗しました:\n{str(e)}")
