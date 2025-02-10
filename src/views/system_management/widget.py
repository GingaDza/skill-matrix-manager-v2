"""
システム管理タブのウィジェット
Created: 2025-02-09 01:36:59
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, 
    QPushButton, QGridLayout, QListWidget,
    QHBoxLayout, QFrame
)
from datetime import datetime
import platform
import psutil

class SystemManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # タブウィジェットの作成
        tab_widget = QTabWidget()
        
        # 各タブの追加
        tab_widget.addTab(self._create_initial_settings_tab(), "初期設定")
        tab_widget.addTab(self._create_data_io_tab(), "データ入出力")
        tab_widget.addTab(self._create_system_info_tab(), "システム情報")
        
        layout.addWidget(tab_widget)
        
    def _create_initial_settings_tab(self):
        """初期設定タブの作成"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # グループリスト
        group_frame = self._create_list_frame("グループリスト")
        layout.addWidget(group_frame)
        
        # 親カテゴリーリスト
        parent_category_frame = self._create_list_frame("親カテゴリーリスト")
        layout.addWidget(parent_category_frame)
        
        # 子カテゴリーリスト
        child_category_frame = self._create_list_frame("子カテゴリーリスト")
        layout.addWidget(child_category_frame)
        
        # メインレイアウトを作成
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        
        # 新規タブ追加ボタン
        add_tab_button = QPushButton("新規タブ追加")
        add_tab_button.clicked.connect(self._on_add_tab_clicked)
        main_layout.addWidget(add_tab_button)
        
        container = QWidget()
        container.setLayout(main_layout)
        return container
        
    def _create_list_frame(self, title):
        """リストフレームの作成"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        layout = QVBoxLayout(frame)
        
        # タイトル
        layout.addWidget(QLabel(title))
        
        # リストウィジェット
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        
        # ボタングループ
        button_layout = QVBoxLayout()
        button_layout.addWidget(QPushButton("追加"))
        button_layout.addWidget(QPushButton("編集"))
        button_layout.addWidget(QPushButton("削除"))
        layout.addLayout(button_layout)
        
        return frame
        
    def _create_data_io_tab(self):
        """データ入出力タブの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # インポートセクション
        import_group = QFrame()
        import_group.setFrameStyle(QFrame.Panel | QFrame.Raised)
        import_layout = QVBoxLayout(import_group)
        import_layout.addWidget(QLabel("データのインポート"))
        import_layout.addWidget(QPushButton("グループリストのインポート"))
        import_layout.addWidget(QPushButton("親カテゴリーリストのインポート"))
        import_layout.addWidget(QPushButton("子カテゴリーリストのインポート"))
        import_layout.addWidget(QPushButton("スキルレベルデータのインポート"))
        layout.addWidget(import_group)
        
        # エクスポートセクション
        export_group = QFrame()
        export_group.setFrameStyle(QFrame.Panel | QFrame.Raised)
        export_layout = QVBoxLayout(export_group)
        export_layout.addWidget(QLabel("データのエクスポート"))
        export_layout.addWidget(QPushButton("レーダーチャート一覧のPDF出力"))
        export_layout.addWidget(QPushButton("全データのCSVエクスポート"))
        layout.addWidget(export_group)
        
        return widget
        
    def _create_system_info_tab(self):
        """システム情報タブの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        info_layout = QVBoxLayout(info_frame)
        
        # システム情報の表示
        system_info = [
            f"アプリケーション: Skill Matrix Manager v2",
            f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"OS: {platform.system()} {platform.release()}",
            f"Python: {platform.python_version()}",
            f"メモリ使用率: {psutil.virtual_memory().percent}%",
            f"CPU使用率: {psutil.cpu_percent()}%",
            f"ログインユーザー: GingaDza",
            f"データベースパス: data/skill_matrix.db"
        ]
        
        for info in system_info:
            info_layout.addWidget(QLabel(info))
            
        layout.addWidget(info_frame)
        return widget
        
    def _on_add_tab_clicked(self):
        """新規タブ追加ボタンのクリックハンドラ"""
        # TODO: 新規タブの追加処理を実装
        pass