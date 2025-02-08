"""メインウィンドウ
Created: 2025-02-08 20:41:10
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QMessageBox, QSplitter, QComboBox,
    QListWidget, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from ..utils.logger import setup_logger
from ..utils.system_info import SystemInfo
from ..database.user_manager import UserManager
from ..database.group_manager import GroupManager
from .tabs.system_tab import SystemTab
from .tabs.category_tab import CategoryTab
from .tabs.data_io_tab import DataIOTab
from .tabs.radar_chart_tab import RadarChartTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(__name__)
        self.system_info = SystemInfo()
        self.user_manager = UserManager()
        self.group_manager = GroupManager()
        self._init_ui()
        self._load_initial_data()

    def _init_ui(self):
        self.setWindowTitle(f"Skill Matrix Manager - v{self.system_info.app_version}")
        self.setGeometry(100, 100, 1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 3:7分割のスプリッター
        splitter = QSplitter(Qt.Horizontal)
        
        # 左パネル（3）
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右パネル（7）
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # 分割比率の設定
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)

        self.statusBar().showMessage(
            f"ログインユーザー: {self.system_info.current_user} | "
            f"最終更新: {self.system_info.current_time}"
        )

    def _create_left_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # グループ選択
        group_layout = QVBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self._on_group_changed)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)

        # ユーザーリスト
        layout.addWidget(QLabel("ユーザー:"))
        self.user_list = QListWidget()
        self.user_list.currentItemChanged.connect(self._on_user_selected)
        layout.addWidget(self.user_list)

        # ユーザー操作ボタン
        button_layout = QVBoxLayout()
        for label, slot in [
            ("ユーザー追加", self._add_user),
            ("ユーザー編集", self._edit_user),
            ("ユーザー削除", self._delete_user)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            button_layout.addWidget(btn)
        layout.addLayout(button_layout)

        return widget

    def _create_right_panel(self):
        self.tab_widget = QTabWidget()
        
        # システム管理タブ
        self.system_tab = SystemTab(self.system_info)
        self.tab_widget.addTab(self.system_tab, "システム管理")
        
        # カテゴリー管理タブ
        self.category_tab = CategoryTab()
        self.tab_widget.addTab(self.category_tab, "カテゴリー管理")
        
        # データ入出力タブ
        self.data_io_tab = DataIOTab()
        self.tab_widget.addTab(self.data_io_tab, "データ入出力")
        
        # レーダーチャートタブ
        self.radar_tab = RadarChartTab()
        self.tab_widget.addTab(self.radar_tab, "総合評価")

        return self.tab_widget

    def _load_initial_data(self):
        """初期データの読み込み"""
        self._load_groups()
        self._load_users()

    def _load_groups(self):
        """グループ一覧の読み込み"""
        self.group_combo.clear()
        groups = self.group_manager.get_all_groups()
        for group in groups:
            self.group_combo.addItem(group.name, group.id)

    def _load_users(self):
        """ユーザー一覧の読み込み"""
        self.user_list.clear()
        group_id = self.group_combo.currentData()
        if group_id:
            users = self.user_manager.get_users_by_group(group_id)
            for user in users:
                self.user_list.addItem(user.name)

    def _add_user(self):
        """ユーザーの追加"""
        from .dialogs.user_dialog import UserDialog
        dialog = UserDialog(self)
        if dialog.exec_():
            self._load_users()

    def _edit_user(self):
        """ユーザーの編集"""
        current = self.user_list.currentItem()
        if not current:
            QMessageBox.warning(self, "選択エラー", "編集するユーザーを選択してください。")
            return
        
        from .dialogs.user_dialog import UserDialog
        dialog = UserDialog(self, current.text())
        if dialog.exec_():
            self._load_users()

    def _delete_user(self):
        """ユーザーの削除"""
        current = self.user_list.currentItem()
        if not current:
            QMessageBox.warning(self, "選択エラー", "削除するユーザーを選択してください。")
            return
        
        reply = QMessageBox.question(
            self,
            "削除確認",
            f"ユーザー '{current.text()}' を削除しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: 削除処理の実装
            self._load_users()

    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        reply = QMessageBox.question(
            self,
            '確認',
            "アプリケーションを終了しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.logger.info("アプリケーションを終了します")
            event.accept()
        else:
            event.ignore()
