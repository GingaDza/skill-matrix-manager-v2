"""システム管理タブ
Created: 2025-02-08 14:27:10
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox
)
from ...utils.system_info import SystemInfo
from ...database.database_manager import DatabaseManager
from ...utils.logger import setup_logger

class SystemTab(QWidget):
    """システム管理タブ"""

    def __init__(self, system_info: SystemInfo, parent=None):
        """初期化
        
        Args:
            system_info (SystemInfo): システム情報
            parent (QWidget, optional): 親ウィジェット
        """
        super().__init__(parent)
        self.logger = setup_logger(__name__)
        self.system_info = system_info
        self.db_manager = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)

        # システム情報グループ
        system_group = QGroupBox("システム情報")
        system_layout = QVBoxLayout(system_group)
        
        info = self.system_info.app_info
        system_layout.addWidget(QLabel(f"バージョン: {info['version']}"))
        system_layout.addWidget(QLabel(f"ユーザー: {info['user']}"))
        system_layout.addWidget(QLabel(f"最終更新: {info['timestamp']}"))
        
        layout.addWidget(system_group)

        # データベース情報グループ
        db_group = QGroupBox("データベース情報")
        db_layout = QVBoxLayout(db_group)
        
        db_status = self.system_info.get_system_status()['database']
        db_layout.addWidget(QLabel(f"データベース名: {db_status['name']}"))
        db_layout.addWidget(QLabel(f"バージョン: {db_status['version']}"))
        
        layout.addWidget(db_group)

        # ログ情報グループ
        log_group = QGroupBox("ログ情報")
        log_layout = QVBoxLayout(log_group)
        
        log_status = self.system_info.get_system_status()['logging']
        log_layout.addWidget(QLabel(f"バージョン: {log_status['version']}"))
        log_layout.addWidget(QLabel("ハンドラー:"))
        for handler, config in log_status['handlers'].items():
            log_layout.addWidget(QLabel(f"  - {handler}: {config['level']}"))
        
        layout.addWidget(log_group)

        # メンテナンスグループ
        maintenance_group = QGroupBox("メンテナンス")
        maintenance_layout = QVBoxLayout(maintenance_group)
        
        backup_button = QPushButton("データベースのバックアップ")
        backup_button.clicked.connect(self._backup_database)
        maintenance_layout.addWidget(backup_button)
        
        layout.addWidget(maintenance_group)
        
        layout.addStretch()

    def _backup_database(self):
        """データベースのバックアップ"""
        self.logger.info("データベースのバックアップを開始します")
        # TODO: バックアップ処理の実装
