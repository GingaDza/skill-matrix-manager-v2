"""システム情報タブモジュール"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from ...database import DatabaseManager
from ...utils.system_info import SystemInfo

class SystemInfoTab(QWidget):
    """システム情報タブ"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.system_info = SystemInfo()
        self.logger = logging.getLogger(__name__)
        self.debug_mode = False
        self.setup_ui()
        self._setup_auto_refresh()
        
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # ヘッダー
        header = QLabel("システム情報")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # メインコンテンツウィジェット
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # バージョン情報
        version_frame = self._create_section("バージョン情報")
        version_layout = QVBoxLayout()
        self.version_label = QLabel()
        version_layout.addWidget(self.version_label)
        version_frame.setLayout(version_layout)
        content_layout.addWidget(version_frame)
        
        # データベース情報
        db_frame = self._create_section("データベース情報")
        db_layout = QVBoxLayout()
        self.db_label = QLabel()
        db_layout.addWidget(self.db_label)
        db_frame.setLayout(db_layout)
        content_layout.addWidget(db_frame)
        
        # システム統計
        stats_frame = self._create_section("システム統計")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel()
        stats_layout.addWidget(self.stats_label)
        stats_frame.setLayout(stats_layout)
        content_layout.addWidget(stats_frame)
        
        # デバッグ情報
        debug_frame = self._create_section("デバッグ情報")
        debug_layout = QVBoxLayout()
        
        debug_header = QHBoxLayout()
        debug_toggle = QPushButton("デバッグモード切替")
        debug_toggle.clicked.connect(self._toggle_debug)
        debug_header.addWidget(debug_toggle)
        debug_header.addStretch()
        debug_layout.addLayout(debug_header)
        
        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)
        self.debug_text.setVisible(False)
        debug_layout.addWidget(self.debug_text)
        
        debug_frame.setLayout(debug_layout)
        content_layout.addWidget(debug_frame)
        
        # 更新ボタン
        refresh_btn = QPushButton("情報を更新")
        refresh_btn.clicked.connect(self._refresh_system_info)
        content_layout.addWidget(refresh_btn)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self._update_system_info()
        
    def _create_section(self, title):
        """セクションフレームの作成"""
        section = QFrame()
        section.setFrameStyle(QFrame.Panel | QFrame.Raised)
        section.setLineWidth(1)
        
        # セクションタイトル
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        section.setLayout(layout)
        
        return section
        
    def _toggle_debug(self):
        """デバッグモードの切り替え"""
        self.debug_mode = not self.debug_mode
        self.debug_text.setVisible(self.debug_mode)
        self._log_debug(f"デバッグモード: {'有効' if self.debug_mode else '無効'}")
        
    def _update_system_info(self):
        """システム情報の更新"""
        try:
            # バージョン情報
            self.version_label.setText(
                f"アプリケーション: v{self.system_info.get_app_version()}\n"
                f"最終更新: {self.system_info.get_current_time_utc()}"
            )
            
            # データベース情報
            self.db_label.setText(
                f"パス: {self.db_manager.db_path}\n"
                f"接続状態: 接続済み"
            )
            
            # システム統計
            stats = self._get_system_stats()
            self.stats_label.setText(
                f"グループ数: {stats['groups']}\n"
                f"ユーザー数: {stats['users']}\n"
                f"カテゴリー数: {stats['categories']}\n"
                f"スキル数: {stats['skills']}"
            )
            
        except Exception as e:
            self.logger.error(f"システム情報の更新に失敗: {e}")
            self._log_debug(f"エラー: {e}")
            
    def _get_system_stats(self):
        """システム統計の取得"""
        try:
            return {
                'groups': len(self.db_manager.get_groups()),
                'users': 0,  # 実装予定
                'categories': len(self.db_manager.get_categories()),
                'skills': len(self.db_manager.get_skills())
            }
        except Exception as e:
            self.logger.error(f"統計情報の取得に失敗: {e}")
            return {
                'groups': 0,
                'users': 0,
                'categories': 0,
                'skills': 0
            }
            
    def _log_debug(self, message):
        """デバッグ情報のログ出力"""
        if self.debug_mode and hasattr(self, 'debug_text'):
            current_text = self.debug_text.toPlainText()
            timestamp = datetime.now().strftime('%H:%M:%S')
            new_message = f"[{timestamp}] {message}\n"
            self.debug_text.setText(current_text + new_message)
            self.logger.debug(message)
            
    def _setup_auto_refresh(self):
        """自動更新タイマーの設定"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._update_system_info)
        self.refresh_timer.start(60000)  # 1分ごとに更新
        self.logger.debug("自動更新タイマーを設定しました")
        
    def _refresh_system_info(self):
        """手動更新処理"""
        self._update_system_info()
        self._log_debug("システム情報を手動で更新しました")
        
    def closeEvent(self, event):
        """ウィンドウクローズ時の処理"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()
