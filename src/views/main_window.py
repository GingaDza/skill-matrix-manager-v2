"""
メインウィンドウ実装
Created: 2025-02-09 09:32:46
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QListWidget, QPushButton,
    QDialog, QLineEdit, QMessageBox, QTabWidget,
    QSpinBox, QFrame, QGridLayout, QListWidgetItem
)
from PyQt5.QtCore import Qt
from .custom_widgets.radar_chart import RadarChartWidget
from .custom_widgets.skill_grid import SkillGridWidget

class MainWindow(QMainWindow):
    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_user_id = None
        self.categories = []
        self.skill_grids = {}
        self.init_ui()
        if self.db:
            self.refresh_groups()
            self.refresh_categories()

    def init_ui(self):
        """UIの初期化"""
        self.setWindowTitle("スキルマトリックスマネージャー")
        self.setGeometry(100, 100, 1200, 800)
        
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        layout = QHBoxLayout(main_widget)
        
        # 左側のパネル（グループとユーザー）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ管理セクション
        left_layout.addWidget(self._create_group_section())
        
        # ユーザー管理セクション
        left_layout.addWidget(self._create_user_section())
        
        layout.addWidget(left_panel, stretch=1)
        
        # 右側のパネル（スキル管理）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # カテゴリー管理セクション
        right_layout.addWidget(self._create_category_section())
        
        # スキル管理タブ
        self.skill_tabs = QTabWidget()
        right_layout.addWidget(self.skill_tabs)
        
        # レーダーチャート
        self.radar_chart = RadarChartWidget(["未設定"])
        right_layout.addWidget(self.radar_chart)
        
        layout.addWidget(right_panel, stretch=2)

    def _create_section(self, title):
        """セクションの作成"""
        section = QFrame()
        section.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        layout = QVBoxLayout(section)
        
        # タイトル
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)
        
        return section, layout

    def _create_group_section(self):
        """グループ管理セクションの作成"""
        section, layout = self._create_section("グループ管理")
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel('グループ:'))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_selected)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        add_group_btn = QPushButton('グループ追加')
        add_group_btn.clicked.connect(self.show_add_group_dialog)
        button_layout.addWidget(add_group_btn)
        layout.addLayout(button_layout)
        
        return section

    def _create_user_section(self):
        """ユーザー管理セクションの作成"""
        section, layout = self._create_section("ユーザー管理")
        
        # ユーザーリスト
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        layout.addWidget(self.user_list)
        
        # ボタン
        button_layout = QHBoxLayout()
        add_user_btn = QPushButton('ユーザー追加')
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        button_layout.addWidget(add_user_btn)
        layout.addLayout(button_layout)
        
        return section

    def _create_category_section(self):
        """カテゴリー管理セクションの作成"""
        section, layout = self._create_section("カテゴリー管理")
        
        # カテゴリーリスト
        self.category_list = QListWidget()
        layout.addWidget(self.category_list)
        
        # ボタン
        button_layout = QHBoxLayout()
        add_category_btn = QPushButton('カテゴリー追加')
        add_category_btn.clicked.connect(self.show_add_category_dialog)
        button_layout.addWidget(add_category_btn)
        layout.addLayout(button_layout)
        
        return section

    def _create_skill_tab(self, category_id, category_name):
        """スキルタブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # スキルグリッド
        skills = self.db.get_skills_in_category(category_id)
        skill_names = [skill[1] for skill in skills]
        grid = SkillGridWidget(skill_names)
        grid.skillLevelsChanged.connect(
            lambda levels: self._update_skill_levels(category_id, levels)
        )
        
        layout.addWidget(grid)
        
        # スキル追加ボタン
        add_skill_btn = QPushButton('スキル追加')
        add_skill_btn.clicked.connect(
            lambda: self.show_add_skill_dialog(category_id)
        )
        layout.addWidget(add_skill_btn)
        
        return tab, grid

    def refresh_groups(self):
        """グループリストの更新"""
        if not self.db:
            return
        
        self.group_combo.clear()
        groups = self.db.get_groups()
        for group_id, group_name in groups:
            self.group_combo.addItem(group_name, group_id)

    def refresh_users(self):
        """ユーザーリストの更新"""
        if not self.db:
            return
        
        self.user_list.clear()
        group_id = self.group_combo.currentData()
        if group_id is not None:
            users = self.db.get_users_in_group(group_id)
            for user_id, user_name in users:
                item = QListWidgetItem(user_name, self.user_list)
                item.setData(Qt.UserRole, user_id)

    def refresh_categories(self):
        """カテゴリーの更新"""
        if not self.db:
            return
        
        try:
            self.category_list.clear()
            categories = self.db.get_categories()
            self.categories = [cat[1] for cat in categories]
            for cat_id, cat_name in categories:
                item = QListWidgetItem(cat_name)
                item.setData(Qt.UserRole, cat_id)
                self.category_list.addItem(item)
            
            self.radar_chart.set_categories(self.categories)
            self.update_skill_view()
        except Exception as e:
            QMessageBox.warning(self, 'エラー', f'カテゴリーの更新に失敗しました: {e}')

    def show_add_group_dialog(self):
        """グループ追加ダイアログの表示"""
        dialog = QDialog(self)
        dialog.setWindowTitle('グループ追加')
        layout = QVBoxLayout(dialog)
        
        # 入力フィールド
        name_edit = QLineEdit()
        layout.addWidget(QLabel('グループ名:'))
        layout.addWidget(name_edit)
        
        # ボタン
        button_box = QHBoxLayout()
        ok_btn = QPushButton('追加')
        cancel_btn = QPushButton('キャンセル')
        
        ok_btn.clicked.connect(lambda: self._add_group(name_edit.text(), dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        dialog.exec_()

    def show_add_user_dialog(self):
        """ユーザー追加ダイアログの表示"""
        if self.group_combo.currentData() is None:
            QMessageBox.warning(self, 'エラー', 'グループを選択してください')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle('ユーザー追加')
        layout = QVBoxLayout(dialog)
        
        # 入力フィールド
        name_edit = QLineEdit()
        layout.addWidget(QLabel('ユーザー名:'))
        layout.addWidget(name_edit)
        
        # ボタン
        button_box = QHBoxLayout()
        ok_btn = QPushButton('追加')
        cancel_btn = QPushButton('キャンセル')
        
        ok_btn.clicked.connect(lambda: self._add_user(name_edit.text(), dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        dialog.exec_()

    def show_add_category_dialog(self):
        """カテゴリー追加ダイアログの表示"""
        dialog = QDialog(self)
        dialog.setWindowTitle('カテゴリー追加')
        layout = QVBoxLayout(dialog)
        
        # 入力フィールド
        name_edit = QLineEdit()
        layout.addWidget(QLabel('カテゴリー名:'))
        layout.addWidget(name_edit)
        
        # ボタン
        button_box = QHBoxLayout()
        ok_btn = QPushButton('追加')
        cancel_btn = QPushButton('キャンセル')
        
        ok_btn.clicked.connect(lambda: self._add_category(name_edit.text(), dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        dialog.exec_()

    def show_add_skill_dialog(self, category_id):
        """スキル追加ダイアログの表示"""
        dialog = QDialog(self)
        dialog.setWindowTitle('スキル追加')
        layout = QVBoxLayout(dialog)
        
        # 入力フィールド
        name_edit = QLineEdit()
        layout.addWidget(QLabel('スキル名:'))
        layout.addWidget(name_edit)
        
        # ボタン
        button_box = QHBoxLayout()
        ok_btn = QPushButton('追加')
        cancel_btn = QPushButton('キャンセル')
        
        ok_btn.clicked.connect(
            lambda: self._add_skill(category_id, name_edit.text(), dialog)
        )
        cancel_btn.clicked.connect(dialog.reject)
        
        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        dialog.exec_()

    def _add_group(self, name, dialog):
        """グループの追加"""
        if not name:
            QMessageBox.warning(dialog, 'エラー', 'グループ名を入力してください')
            return
        
        try:
            self.db.add_group(name)
            self.refresh_groups()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, 'エラー', f'グループの追加に失敗しました: {e}')

    def _add_user(self, name, dialog):
        """ユーザーの追加"""
        if not name:
            QMessageBox.warning(dialog, 'エラー', 'ユーザー名を入力してください')
            return
        
        try:
            group_id = self.group_combo.currentData()
            self.db.add_user(name, group_id)
            self.refresh_users()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, 'エラー', f'ユーザーの追加に失敗しました: {e}')

    def _add_category(self, name, dialog):
        """カテゴリーの追加"""
        if not name:
            QMessageBox.warning(dialog, 'エラー', 'カテゴリー名を入力してください')
            return
        
        try:
            self.db.add_category(name)
            self.refresh_categories()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, 'エラー', f'カテゴリーの追加に失敗しました: {e}')

    def _add_skill(self, category_id, name, dialog):
        """スキルの追加"""
        if not name:
            QMessageBox.warning(dialog, 'エラー', 'スキル名を入力してください')
            return
        
        try:
            self.db.add_skill(name, category_id)
            self.update_skill_view()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, 'エラー', f'スキルの追加に失敗しました: {e}')

    def _update_skill_levels(self, category_id, levels):
        """スキルレベルの更新"""
        if not self.current_user_id:
            return
        
        try:
            for skill_name, level in levels.items():
                skill_id = self.db.get_skill_id(category_id, skill_name)
                if skill_id:
                    self.db.update_skill_level(
                        self.current_user_id, skill_id, level
                    )
            
            # レーダーチャートの更新
            self.update_radar_chart()
        except Exception as e:
            QMessageBox.warning(
                self, 'エラー', f'スキルレベルの更新に失敗しました: {e}'
            )

    def on_group_selected(self, index):
        """グループ選択時の処理"""
        self.refresh_users()
        self.current_user_id = None
        self.update_skill_view()

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        current_item = self.user_list.currentItem()
        if current_item:
            self.current_user_id = current_item.data(Qt.UserRole)
            self.update_skill_view()

    def update_skill_view(self):
        """スキルビューの更新"""
        try:
            # タブをクリア
            self.skill_tabs.clear()
            
            # カテゴリごとにタブを作成
            self.skill_grids = {}  # カテゴリIDごとのグリッドを保持
            categories = self.db.get_categories()
            
            for category_id, category_name in categories:
                tab, grid = self._create_skill_tab(category_id, category_name)
                self.skill_tabs.addTab(tab, category_name)
                self.skill_grids[category_id] = grid
            
            # 現在のユーザーのスキルレベルを設定
            if self.current_user_id:
                self.load_user_skills()
        
        except Exception as e:
            QMessageBox.warning(
                self, 'エラー', f'スキルビューの更新に失敗しました: {e}'
            )
    
    def load_user_skills(self):
        """ユーザーのスキルレベルを読み込み"""
        try:
            for category_id, grid in self.skill_grids.items():
                skills = self.db.get_user_skills(
                    self.current_user_id, category_id
                )
                levels = {skill[0]: skill[1] for skill in skills}
                grid.set_levels(levels)
            
            # レーダーチャートの更新
            self.update_radar_chart()
        
        except Exception as e:
            QMessageBox.warning(
                self, 'エラー', f'スキルレベルの読み込みに失敗しました: {e}'
            )
    
    def update_radar_chart(self):
        """レーダーチャートの更新"""
        try:
            if not self.current_user_id:
                self.radar_chart.update_data([0] * len(self.categories))
                return
            
            # カテゴリごとの平均スキルレベルを計算
            levels = []
            for category_id, _ in self.db.get_categories():
                skills = self.db.get_user_skills(
                    self.current_user_id, category_id
                )
                if skills:
                    avg_level = sum(skill[1] for skill in skills) / len(skills)
                    levels.append(avg_level)
                else:
                    levels.append(0)
            
            self.radar_chart.update_data(levels)
        
        except Exception as e:
            QMessageBox.warning(
                self, 'エラー', f'レーダーチャートの更新に失敗しました: {e}'
            )