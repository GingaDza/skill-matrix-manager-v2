"""
システム管理タブ
Created: 2025-02-09 13:31:08
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QFileDialog, QListWidget,
    QMessageBox, QGroupBox, QComboBox, QSpacerItem,
    QSizePolicy, QTableWidget, QTableWidgetItem
)
from ..custom_widgets.radar_chart import RadarChart

class SystemTab(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # タブウィジェットの作成
        tab_widget = QTabWidget()
        
        # 1-1: 初期設定タブ
        settings_tab = self.create_settings_tab()
        tab_widget.addTab(settings_tab, "初期設定")
        
        # 1-2: データ入出力タブ
        io_tab = self.create_io_tab()
        tab_widget.addTab(io_tab, "データ入出力")
        
        # 1-3: スキルギャップ設定タブ
        skill_gap_tab = self.create_skill_gap_tab()
        tab_widget.addTab(skill_gap_tab, "スキルギャップ設定")
        
        # 1-4: システム情報タブ
        info_tab = self.create_info_tab()
        tab_widget.addTab(info_tab, "システム情報")
        
        layout.addWidget(tab_widget)

    def create_settings_tab(self):
        """初期設定タブの作成"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # 左側：グループリスト
        group_box = QGroupBox("グループ管理")
        group_layout = QVBoxLayout(group_box)
        
        self.group_list = QListWidget()
        group_layout.addWidget(self.group_list)
        
        group_buttons = QHBoxLayout()
        add_group_btn = QPushButton("追加")
        edit_group_btn = QPushButton("編集")
        delete_group_btn = QPushButton("削除")
        
        for btn in [add_group_btn, edit_group_btn, delete_group_btn]:
            btn.setFixedWidth(60)
            group_buttons.addWidget(btn)
        
        group_layout.addLayout(group_buttons)
        layout.addWidget(group_box)
        
        # 中央：カテゴリー管理
        category_box = QGroupBox("カテゴリー管理")
        category_layout = QVBoxLayout(category_box)
        
        # 親カテゴリー
        category_layout.addWidget(QLabel("親カテゴリー"))
        self.parent_category_list = QListWidget()
        category_layout.addWidget(self.parent_category_list)
        
        parent_buttons = QHBoxLayout()
        add_parent_btn = QPushButton("追加")
        edit_parent_btn = QPushButton("編集")
        delete_parent_btn = QPushButton("削除")
        
        for btn in [add_parent_btn, edit_parent_btn, delete_parent_btn]:
            btn.setFixedWidth(60)
            parent_buttons.addWidget(btn)
        
        category_layout.addLayout(parent_buttons)
        
        # 子カテゴリー
        category_layout.addWidget(QLabel("子カテゴリー"))
        self.child_category_list = QListWidget()
        category_layout.addWidget(self.child_category_list)
        
        child_buttons = QHBoxLayout()
        add_child_btn = QPushButton("追加")
        edit_child_btn = QPushButton("編集")
        delete_child_btn = QPushButton("削除")
        
        for btn in [add_child_btn, edit_child_btn, delete_child_btn]:
            btn.setFixedWidth(60)
            child_buttons.addWidget(btn)
        
        category_layout.addLayout(child_buttons)
        layout.addWidget(category_box)
        
        # 右側：新規タブ管理
        tab_box = QGroupBox("新規タブ管理")
        tab_layout = QVBoxLayout(tab_box)
        
        add_tab_btn = QPushButton("新規タブ追加")
        add_tab_btn.clicked.connect(self.add_new_tab)
        tab_layout.addWidget(add_tab_btn)
        
        tab_layout.addStretch()
        layout.addWidget(tab_box)
        
        return tab

    def create_io_tab(self):
        """データ入出力タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # インポート設定
        import_group = QGroupBox("データインポート")
        import_layout = QVBoxLayout(import_group)
        
        import_type = QComboBox()
        import_type.addItems([
            "グループリスト",
            "親カテゴリーリスト",
            "子カテゴリーリスト",
            "スキルレベルデータ"
        ])
        import_layout.addWidget(import_type)
        
        import_btn = QPushButton("インポート")
        import_btn.clicked.connect(self.import_data)
        import_layout.addWidget(import_btn)
        
        layout.addWidget(import_group)
        
        # エクスポート設定
        export_group = QGroupBox("データエクスポート")
        export_layout = QVBoxLayout(export_group)
        
        export_type = QComboBox()
        export_type.addItems([
            "レーダーチャート一覧",
            "スキルレベルデータ",
            "全データ"
        ])
        export_layout.addWidget(export_type)
        
        export_btn = QPushButton("エクスポート")
        export_btn.clicked.connect(self.export_data)
        export_layout.addWidget(export_btn)
        
        layout.addWidget(export_group)
        
        layout.addStretch()
        return tab

    def create_skill_gap_tab(self):
        """スキルギャップ設定タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # カテゴリー選択セクション
        category_group = QGroupBox("カテゴリー選択")
        category_layout = QVBoxLayout(category_group)
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("全カテゴリー")
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        category_layout.addWidget(self.category_combo)
        
        layout.addWidget(category_group)
        
        # スキルレベル設定セクション
        skill_group = QGroupBox("目標スキルレベル設定")
        skill_layout = QVBoxLayout(skill_group)
        
        self.skill_table = QTableWidget()
        self.skill_table.setColumnCount(3)
        self.skill_table.setHorizontalHeaderLabels(["スキル", "現在の目標", "新しい目標"])
        self.skill_table.itemChanged.connect(self.on_skill_level_changed)
        skill_layout.addWidget(self.skill_table)
        
        layout.addWidget(skill_group)
        
        # プレビューセクション
        preview_group = QGroupBox("プレビュー")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_chart = RadarChart()
        preview_layout.addWidget(self.preview_chart)
        layout.addWidget(preview_group)
        
        # ボタンセクション
        button_layout = QHBoxLayout()
        save_btn = QPushButton("設定を保存")
        save_btn.clicked.connect(self.save_skill_gap_settings)
        reset_btn = QPushButton("設定をリセット")
        reset_btn.clicked.connect(self.reset_skill_gap_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        
        # 初期データの読み込み
        self.load_skill_gap_data()
        
        return tab

    def create_info_tab(self):
        """システム情報タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # システム情報
        info_group = QGroupBox("システム情報")
        info_layout = QVBoxLayout(info_group)
        
        info_layout.addWidget(QLabel("アプリケーション名: スキルマトリックスマネージャー"))
        info_layout.addWidget(QLabel("バージョン: 2.0.0"))
        info_layout.addWidget(QLabel("作成者: GingaDza"))
        
        # データベース情報
        db_info = QGroupBox("データベース情報")
        db_layout = QVBoxLayout(db_info)
        db_layout.addWidget(QLabel("データベース: SQLite"))
        db_layout.addWidget(QLabel("場所: skill_matrix.db"))
        info_layout.addWidget(db_info)
        
        layout.addWidget(info_group)
        layout.addStretch()
        
        return tab

    def on_category_changed(self, index):
        """カテゴリー変更時の処理"""
        try:
            self.update_skill_table()
            self.update_skill_gap_preview()
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"カテゴリーの更新に失敗しました: {str(e)}")

    def on_skill_level_changed(self, item):
        """スキルレベル変更時の処理"""
        if item.column() == 2:  # 新しい目標列
            self.update_skill_gap_preview()

    def load_skill_gap_data(self):
        """スキルギャップデータの読み込み"""
        try:
            # サンプルデータ（後でデータベースから取得）
            self.update_skill_gap_preview()
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"データの読み込みに失敗しました: {str(e)}")

    def update_skill_gap_preview(self):
        """プレビューの更新"""
        try:
            # サンプルデータ
            current_data = {
                "Python": 3,
                "JavaScript": 2,
                "SQL": 4,
                "UI設計": 3,
                "テスト": 2
            }
            
            target_data = {
                "Python": 4,
                "JavaScript": 4,
                "SQL": 5,
                "UI設計": 4,
                "テスト": 4
            }
            
            self.preview_chart.update_data(current_data, target_data)
            
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"プレビューの更新に失敗しました: {str(e)}")

    def save_skill_gap_settings(self):
        """スキルギャップ設定の保存"""
        try:
            QMessageBox.information(self, "成功", "設定を保存しました")
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"設定の保存に失敗しました: {str(e)}")

    def reset_skill_gap_settings(self):
        """スキルギャップ設定のリセット"""
        try:
            reply = QMessageBox.question(
                self,
                '確認',
                'すべての設定をリセットしますか？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.load_skill_gap_data()
                QMessageBox.information(self, "成功", "設定をリセットしました")
            
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"設定のリセットに失敗しました: {str(e)}")

    def import_data(self):
        """データのインポート"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "データインポート",
                "",
                "Excel Files (*.xlsx);;CSV Files (*.csv)"
            )
            if file_path:
                QMessageBox.information(self, "成功", "データをインポートしました")
        except Exception as e:
            QMessageBox.warning(
                self,
                "エラー",
                f"データのインポートに失敗しました: {str(e)}"
            )

    def export_data(self):
        """データのエクスポート"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "データエクスポート",
                "",
                "PDF Files (*.pdf);;Excel Files (*.xlsx);;CSV Files (*.csv)"
            )
            if file_path:
                QMessageBox.information(self, "成功", "データをエクスポートしました")
        except Exception as e:
            QMessageBox.warning(
                self,
                "エラー",
                f"データのエクスポートに失敗しました: {str(e)}"
            )

    def add_new_tab(self):
        """新規タブの追加"""
        try:
            selected_category = self.parent_category_list.currentItem()
            if not selected_category:
                raise ValueError("親カテゴリーを選択してください")
            
            QMessageBox.information(self, "成功", "新規タブを追加しました")
        except Exception as e:
            QMessageBox.warning(self, "エラー", str(e))
