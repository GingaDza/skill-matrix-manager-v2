"""スキルダイアログモジュール"""
import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

class SkillDialog(QDialog):
    """スキル追加・編集ダイアログ"""
    
    def __init__(self, parent=None, skill=None, categories=None):
        """初期化
        
        Args:
            parent: 親ウィジェット
            skill: 編集する場合のスキルデータ (id, name, description, category_id, category_name)
            categories: カテゴリーのリスト [(id, name, description), ...]
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.skill = skill
        self.categories = categories or []
        self.setup_ui()
        
    def setup_ui(self):
        """UIの初期化"""
        self.setWindowTitle("スキル追加" if not self.skill else "スキル編集")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # スキル名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("スキル名:")
        self.name_edit = QLineEdit()
        if self.skill:
            self.name_edit.setText(self.skill[1])  # name
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # カテゴリー選択
        category_layout = QHBoxLayout()
        category_label = QLabel("カテゴリー:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("カテゴリーを選択", None)
        for cat_id, name, _ in self.categories:
            self.category_combo.addItem(name, cat_id)
        if self.skill and len(self.skill) > 3:
            index = self.category_combo.findData(self.skill[3])  # category_id
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # 説明入力
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        if self.skill:
            self.desc_edit.setText(self.skill[2])  # description
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_edit)
        
        # ボタン
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("キャンセル")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_data(self):
        """ダイアログのデータを取得
        
        Returns:
            tuple: (name, description, category_id)
        """
        name = self.name_edit.text().strip()
        desc = self.desc_edit.toPlainText().strip()
        category_id = self.category_combo.currentData()
        
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "スキル名を入力してください。"
            )
            return None
            
        if not category_id:
            QMessageBox.warning(
                self,
                "入力エラー",
                "カテゴリーを選択してください。"
            )
            return None
            
        return name, desc, category_id
