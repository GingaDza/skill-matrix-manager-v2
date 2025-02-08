"""ユーザーダイアログモジュール"""
import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QComboBox
)

class UserDialog(QDialog):
    """ユーザー追加・編集ダイアログ"""
    
    def __init__(self, parent=None, user=None, groups=None):
        """初期化
        
        Args:
            parent: 親ウィジェット
            user: 編集する場合のユーザーデータ (id, name, email, group_id)
            groups: グループのリスト [(id, name), ...]
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.user = user
        self.groups = groups or []
        self.setup_ui()
        
    def setup_ui(self):
        """UIの初期化"""
        self.setWindowTitle("ユーザー追加" if not self.user else "ユーザー編集")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # ユーザー名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("ユーザー名:")
        self.name_edit = QLineEdit()
        if self.user:
            self.name_edit.setText(self.user[1])  # name
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # メールアドレス入力
        email_layout = QHBoxLayout()
        email_label = QLabel("メールアドレス:")
        self.email_edit = QLineEdit()
        if self.user:
            self.email_edit.setText(self.user[2])  # email
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_edit)
        layout.addLayout(email_layout)
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_label = QLabel("グループ:")
        self.group_combo = QComboBox()
        self.group_combo.addItem("グループを選択", None)
        for group_id, name in self.groups:
            self.group_combo.addItem(name, group_id)
        if self.user and len(self.user) > 3:
            index = self.group_combo.findData(self.user[3])  # group_id
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
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
            tuple: (name, email, group_id)
        """
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        group_id = self.group_combo.currentData()
        
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "ユーザー名を入力してください。"
            )
            return None
            
        if not email:
            QMessageBox.warning(
                self,
                "入力エラー",
                "メールアドレスを入力してください。"
            )
            return None
            
        if not group_id:
            QMessageBox.warning(
                self,
                "入力エラー",
                "グループを選択してください。"
            )
            return None
            
        return name, email, group_id
