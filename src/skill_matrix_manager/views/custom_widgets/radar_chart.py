"""
レーダーチャートウィジェット（スキルギャップ機能付き）
Created: 2025-02-09 13:27:07
Author: GingaDza
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class RadarChart(QWidget):
    """スキルギャップ表示機能付きレーダーチャート"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='polar')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data = {}
        self.target_data = {}
        self.gap_enabled = True
        self.setup_style()

    def setup_style(self):
        """スタイルの設定"""
        self.ax.grid(True, color='gray', alpha=0.3)
        self.ax.set_facecolor('white')
        self.ax.tick_params(axis='both', colors='#333333', labelsize=8)
        self.ax.set_title('スキルレベル比較', pad=15, fontsize=10, color='#333333')

    def update_data(self, current_data, target_data=None, show_gap=True):
        """
        データの更新
        
        Args:
            current_data (dict): 現在のスキルレベルデータ
            target_data (dict): 目標スキルレベルデータ
            show_gap (bool): ギャップを表示するかどうか
        """
        self.data = current_data
        self.target_data = target_data if target_data else {}
        self.gap_enabled = show_gap
        self._draw_chart()

    def _draw_chart(self):
        """チャートの描画"""
        self.ax.clear()
        self.setup_style()
        
        if not self.data:
            return

        categories = list(self.data.keys())
        values = list(self.data.values())
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
        
        # データを円形に
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        
        # 現在のスキルレベル
        self.ax.plot(angles, values, 'o-', linewidth=2,
                    label='現在のレベル', color='#1f77b4')
        self.ax.fill(angles, values, alpha=0.25, color='#1f77b4')
        
        # 目標スキルレベルとギャップの表示
        if self.target_data and self.gap_enabled:
            target_values = [self.target_data.get(cat, 0) for cat in categories]
            target_values = np.concatenate((target_values, [target_values[0]]))
            
            # 目標レベル
            self.ax.plot(angles, target_values, 'o--', linewidth=2,
                        label='目標レベル', color='#ff7f0e')
            
            # ギャップの表示
            gap_values = np.maximum(target_values - values, 0)
            self.ax.fill_between(angles, values, target_values,
                               where=target_values > values,
                               color='#ff9999', alpha=0.3,
                               label='スキルギャップ')
        
        # グリッドの設定
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(categories, fontsize=8)
        self.ax.set_ylim(0, 5)
        self.ax.set_rticks([1, 2, 3, 4, 5])
        
        # 凡例の表示
        if self.target_data and self.gap_enabled:
            self.ax.legend(loc='upper right',
                         bbox_to_anchor=(1.3, 1.1),
                         fontsize=8)
        
        self.figure.tight_layout()
        self.canvas.draw()

    def resizeEvent(self, event):
        """リサイズイベントの処理"""
        super().resizeEvent(event)
        self.figure.tight_layout()
        self.canvas.draw()
