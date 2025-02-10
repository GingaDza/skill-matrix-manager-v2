#!/usr/bin/env python3
"""
開発環境用の実行スクリプト
Created: 2025-02-09 13:10:33
Author: GingaDza
"""
import sys
from PyQt5.QtWidgets import QApplication
from skill_matrix_manager.views.main_window import MainWindow
from skill_matrix_manager.database.manager import DatabaseManager

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    
    # データベースマネージャーの初期化
    db = DatabaseManager("skill_matrix.db")
    
    # メインウィンドウの作成と表示
    window = MainWindow(db)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
