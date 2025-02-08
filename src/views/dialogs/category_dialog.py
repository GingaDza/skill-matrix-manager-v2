"""カテゴリーダイアログモジュール"""
import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox
)

class CategoryDialog(QDialog):
    """カテゴリー追加・編集ダイアログ"""
    
    def __init__(self, parent=None, category=None):
        """初期化
        
        Args:
            parent: 親ウィジェット
            category: 編集する場合のカテゴリーデータ (id, name, description)
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.category = category
        self.setup_ui()
        
    def setup_ui(self):
        """UIの初期化"""
        self.setWindowTitle("カテゴリー追加" if not self.category else "カテゴリー編集")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # カテゴリー名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("カテゴリー名:")
        self.name_edit = QLineEdit()
        if self.category:
            self.name_edit.setText(self.category[1])  # name
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # 説明入力
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        if self.category:
            self.desc_edit.setText(self.category[2])  # description
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
            tuple: (name, description)
        """
        name = self.name_edit.text().strip()
        desc = self.desc_edit.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "カテゴリー名を入力してください。"
            )
            return None
            
        return name, desc
