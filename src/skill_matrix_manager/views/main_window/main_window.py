"""
メインウィンドウの実装
Created: 2025-02-09 13:22:03
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QListWidget,
    QTabWidget, QSplitter, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ..system_tab import SystemTab
from ..evaluation_tab import EvaluationTab

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        # ウィンドウの基本設定
        self.setWindowTitle('スキルマトリックスマネージャー')
        self.setGeometry(100, 100, 1200, 800)
        
        # セントラルウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        
        # スプリッターの作成（3:7の分割）
        splitter = QSplitter(Qt.Horizontal)
        
        # 左パネル（3）
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右パネル（7）
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # スプリッターの比率を3:7に設定
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # ステータスバーの設定
        self.statusBar().showMessage('準備完了')
        
        # 初期データの読み込み
        self.load_initial_data()
    
    def create_left_panel(self):
        """左パネルの作成（グループとユーザー管理）"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # グループセレクター
        group_section = QGroupBox("グループ選択")
        group_layout = QVBoxLayout(group_section)
        
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        group_layout.addWidget(self.group_combo)
        
        # グループ管理ボタン
        group_buttons = QHBoxLayout()
        add_group_btn = QPushButton("追加")
        edit_group_btn = QPushButton("編集")
        delete_group_btn = QPushButton("削除")
        
        for btn in [add_group_btn, edit_group_btn, delete_group_btn]:
            btn.setFixedWidth(60)
            group_buttons.addWidget(btn)
        
        group_layout.addLayout(group_buttons)
        layout.addWidget(group_section)
        
        # ユーザーリスト
        user_section = QGroupBox("ユーザー一覧")
        user_layout = QVBoxLayout(user_section)
        
        self.user_list = QListWidget()
        user_layout.addWidget(self.user_list)
        
        # ユーザー管理ボタン
        user_buttons = QHBoxLayout()
        add_user_btn = QPushButton("追加")
        edit_user_btn = QPushButton("編集")
        delete_user_btn = QPushButton("削除")
        
        for btn in [add_user_btn, edit_user_btn, delete_user_btn]:
            btn.setFixedWidth(60)
            user_buttons.addWidget(btn)
        
        user_layout.addLayout(user_buttons)
        layout.addWidget(user_section)
        
        return panel
    
    def create_right_panel(self):
        """右パネルの作成（タブ付きコンテンツ）"""
        self.tab_widget = QTabWidget()
        
        # システム管理タブ（デフォルト）
        system_tab = SystemTab(self.db)
        self.tab_widget.addTab(system_tab, "システム管理")
        
        # 総合評価タブ
        evaluation_tab = EvaluationTab(self.db)
        self.tab_widget.addTab(evaluation_tab, "総合評価")
        
        return self.tab_widget
    
    def load_initial_data(self):
        """初期データの読み込み"""
        try:
            # グループデータの読み込み
            groups = self.db.get_groups()
            self.group_combo.clear()
            for group_id, group_name in groups:
                self.group_combo.addItem(group_name, group_id)
            
            # 最初のグループを選択
            if self.group_combo.count() > 0:
                self.on_group_changed(0)
        
        except Exception as e:
            QMessageBox.warning(
                self,
                'エラー',
                f'データの読み込みに失敗しました: {str(e)}'
            )
    
    def on_group_changed(self, index):
        """グループ選択時の処理"""
        try:
            group_id = self.group_combo.currentData()
            if group_id is None:
                return
            
            # ユーザーリストの更新
            self.user_list.clear()
            users = self.db.get_users_in_group(group_id)
            for user_id, user_name in users:
                self.user_list.addItem(user_name)
            
            # タブの更新
            self.update_tabs(group_id)
        
        except Exception as e:
            QMessageBox.warning(
                self,
                'エラー',
                f'グループデータの更新に失敗しました: {str(e)}'
            )
    
    def update_tabs(self, group_id):
        """タブの更新"""
        try:
            # カテゴリータブの更新（実装予定）
            pass
        
        except Exception as e:
            QMessageBox.warning(
                self,
                'エラー',
                f'タブの更新に失敗しました: {str(e)}'
            )
    
    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        try:
            # カテゴリータブの実装（後ほど追加）
            pass
        
        except Exception as e:
            QMessageBox.warning(
                self,
                'エラー',
                f'タブの追加に失敗しました: {str(e)}'
            )
