"""システム管理タブ
Created: 2025-02-08 20:41:10
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox
)
from ...utils.system_info import SystemInfo
from ...utils.logger import setup_logger

class SystemTab(QWidget):
    def __init__(self, system_info: SystemInfo, parent=None):
        super().__init__(parent)
        self.logger = setup_logger(__name__)
        self.system_info = system_info
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # システム情報
        info_group = QGroupBox("システム情報")
        info_layout = QVBoxLayout(info_group)
        
        app_info = self.system_info.get_system_status()
        info_layout.addWidget(QLabel(f"アプリケーションバージョン: {self.system_info.app_version}"))
        info_layout.addWidget(QLabel(f"ユーザー: {self.system_info.current_user}"))
        info_layout.addWidget(QLabel(f"最終更新: {self.system_info.current_time}"))
        
        layout.addWidget(info_group)

        # メンテナンス
        maintenance_group = QGroupBox("メンテナンス")
        maintenance_layout = QVBoxLayout(maintenance_group)
        
        backup_btn = QPushButton("データベースのバックアップ")
        backup_btn.clicked.connect(self._backup_database)
        maintenance_layout.addWidget(backup_btn)
        
        layout.addWidget(maintenance_group)
        
        layout.addStretch()

    def _backup_database(self):
        self.logger.info("データベースのバックアップを開始します")
        # TODO: バックアップ処理の実装
