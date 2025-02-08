"""アプリケーションのエントリーポイント
Created: 2025-02-08 20:41:10
Author: GingaDza
"""
import sys
from PyQt5.QtWidgets import QApplication
from .views.main_window import MainWindow
from .utils.logger import setup_logger

def main():
    """メイン関数"""
    logger = setup_logger(__name__)
    logger.info("アプリケーションを開始します")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
