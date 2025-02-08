"""カテゴリー管理タブ
Created: 2025-02-08 14:24:30
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QLabel, QMessageBox
)
from ...database.category_manager import CategoryManager
from ..dialogs.category_dialog import CategoryDialog
from ...utils.logger import setup_logger
from ...models.category import Category

class CategoryTab(QWidget):
    """カテゴリー管理タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = setup_logger(__name__)
        self.category_manager = CategoryManager()
        self._init_ui()
        self._load_categories()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)

        # ツールバー
        toolbar = QHBoxLayout()
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_category)
        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self._edit_category)
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_category)
        toolbar.addWidget(add_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(delete_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # カテゴリーツリー
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["カテゴリー名", "説明"])
        self.tree.setColumnWidth(0, 200)
        layout.addWidget(self.tree)

    def _load_categories(self):
        """カテゴリー一覧の読み込み"""
        self.tree.clear()
        categories = self.category_manager.get_all_categories()
        
        # 親カテゴリーのマップを作成
        category_map = {None: self.tree}
        for category in categories:
            item = QTreeWidgetItem([category.name, category.description or ""])
            item.setData(0, 256, category)  # カスタムデータとしてカテゴリーオブジェクトを保存
            
            parent = category_map.get(category.parent_id, self.tree)
            parent.addChild(item)
            category_map[category.id] = item

        self.tree.expandAll()

    def _add_category(self):
        """カテゴリーの追加"""
        dialog = CategoryDialog(self, category_manager=self.category_manager)
        if dialog.exec_():
            name, parent_id, description = dialog.get_category_data()
            category_id = self.category_manager.create_category(name, parent_id, description)
            if category_id:
                self._load_categories()
                self.logger.info(f"カテゴリー '{name}' を追加しました")

    def _edit_category(self):
        """カテゴリーの編集"""
        current = self.tree.currentItem()
        if not current:
            QMessageBox.warning(self, "選択エラー", "編集するカテゴリーを選択してください。")
            return

        category = current.data(0, 256)
        dialog = CategoryDialog(self, category, self.category_manager)
        if dialog.exec_():
            name, parent_id, description = dialog.get_category_data()
            if self.category_manager.update_category(category.id, name, parent_id, description):
                self._load_categories()
                self.logger.info(f"カテゴリー '{name}' を更新しました")

    def _delete_category(self):
        """カテゴリーの削除"""
        current = self.tree.currentItem()
        if not current:
            QMessageBox.warning(self, "選択エラー", "削除するカテゴリーを選択してください。")
            return

        category = current.data(0, 256)
        reply = QMessageBox.question(
            self,
            "削除確認",
            f"カテゴリー '{category.name}' を削除しますか？\n"
            "※ サブカテゴリーも全て削除されます",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.category_manager.delete_category(category.id):
                self._load_categories()
                self.logger.info(f"カテゴリー '{category.name}' を削除しました")
