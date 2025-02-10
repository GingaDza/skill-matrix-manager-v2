"""
スキルマトリックスマネージャー アプリケーションエントリーポイント
Created: 2025-02-08 22:17:10
Author: GingaDza
"""
import sys
from PyQt5.QtWidgets import QApplication
from .views.main_window import MainWindow
from .utils.logger import setup_logger

def main():
    """アプリケーションのメインエントリーポイント"""
    logger = setup_logger(__name__)
    logger.info("アプリケーションを起動します")
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # モダンなルック&フィールを適用
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()