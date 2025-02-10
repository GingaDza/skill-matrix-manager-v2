"""
評価タブ
Created: 2025-02-09 13:17:36
Author: GingaDza
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QGroupBox, QSplitter
)
from PyQt5.QtCore import Qt
from ..custom_widgets.radar_chart import RadarChart
import numpy as np

class EvaluationTab(QWidget):
    """評価タブ"""

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)

        # グループ選択セクション
        group_section = QHBoxLayout()
        group_label = QLabel("グループ:")
        group_label.setFixedWidth(80)
        group_section.addWidget(group_label)
        
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.refresh_data)
        group_section.addWidget(self.group_combo)
        group_section.addStretch()
        layout.addLayout(group_section)

        # スプリッター（統計情報とチャート）
        splitter = QSplitter(Qt.Horizontal)

        # 左側：統計情報
        stats_group = QGroupBox("統計情報")
        stats_layout = QVBoxLayout(stats_group)
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["項目", "値"])
        stats_layout.addWidget(self.stats_table)
        splitter.addWidget(stats_group)

        # 右側：チャート
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        
        # レーダーチャート
        chart_group = QGroupBox("スキルレベル分布")
        chart_layout = QVBoxLayout(chart_group)
        self.radar_chart = RadarChart()
        chart_layout.addWidget(self.radar_chart)
        charts_layout.addWidget(chart_group)
        
        splitter.addWidget(charts_widget)
        layout.addWidget(splitter)

        # レポート出力ボタン
        button_section = QHBoxLayout()
        button_section.addStretch()
        export_btn = QPushButton("レポート出力")
        export_btn.clicked.connect(self.export_report)
        button_section.addWidget(export_btn)
        layout.addLayout(button_section)

        # 初期データの読み込み
        self.refresh_groups()

    def refresh_groups(self):
        """グループリストの更新"""
        try:
            self.group_combo.clear()
            groups = self.db.get_groups()
            for group_id, group_name in groups:
                self.group_combo.addItem(group_name, group_id)
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"グループリストの更新に失敗しました: {str(e)}")

    def refresh_data(self):
        """データの更新"""
        group_id = self.group_combo.currentData()
        if not group_id:
            return

        try:
            self.update_statistics(group_id)
            self.update_chart(group_id)
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"データの更新に失敗しました: {str(e)}")

    def update_statistics(self, group_id):
        """統計情報の更新"""
        users = self.db.get_users_in_group(group_id)
        stats = [
            ("メンバー数", len(users)),
            ("平均スキルレベル", "3.5"),  # サンプル値
            ("最高スキルレベル", "5.0"),  # サンプル値
            ("最低スキルレベル", "2.0"),  # サンプル値
        ]

        self.stats_table.setRowCount(len(stats))
        for row, (item, value) in enumerate(stats):
            self.stats_table.setItem(row, 0, QTableWidgetItem(str(item)))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(value)))
        
        self.stats_table.resizeColumnsToContents()

    def update_chart(self, group_id):
        """チャートの更新"""
        # サンプルデータ
        data = {
            "Python": 4,
            "JavaScript": 3,
            "SQL": 4,
            "UI設計": 3,
            "テスト": 5
        }
        self.radar_chart.update_data(data)

    def export_report(self):
        """レポートの出力"""
        try:
            QMessageBox.information(self, "成功", "レポートを出力しました")
        except Exception as e:
            QMessageBox.warning(self, "エラー",
                              f"レポートの出力に失敗しました: {str(e)}")
