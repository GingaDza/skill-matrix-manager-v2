"""
オリジナルUI完全コピーのスタイル定義
Created: 2025-02-12 13:12:20
Author: GingaDza
"""

STYLE_SHEET = """
/* メインウィンドウ */
QMainWindow {
    background-color: #ECF0F5;  /* AdminLTE標準背景色 */
}

/* コンテナ */
QWidget#centralWidget {
    background-color: #ECF0F5;
}

/* 左ペイン */
QFrame#leftPane {
    background-color: #FFFFFF;
    margin: 10px;
    border: 1px solid #D2D6DE;
    border-radius: 3px;
}

/* 右ペイン */
QFrame#rightPane {
    background-color: #FFFFFF;
    margin: 10px;
    border: 1px solid #D2D6DE;
    border-radius: 3px;
}

/* グループ選択 */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #D2D6DE;
    border-radius: 3px;
    padding: 5px;
    min-height: 30px;
}

/* リスト */
QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #D2D6DE;
    border-radius: 3px;
    padding: 5px;
}

QListWidget::item {
    height: 30px;
    border-radius: 3px;
    padding: 5px;
}

QListWidget::item:selected {
    background-color: #3C8DBC;
    color: #FFFFFF;
}

/* ボタン */
QPushButton {
    border: none;
    border-radius: 3px;
    padding: 8px 16px;
    min-height: 34px;
    font-size: 14px;
    color: #FFFFFF;
}

QPushButton#add_button {
    background-color: #00A65A;
}

QPushButton#edit_button {
    background-color: #3C8DBC;
}

QPushButton#delete_button {
    background-color: #DD4B39;
}

/* タブ */
QTabWidget::pane {
    border-top: 1px solid #D2D6DE;
    background-color: #FFFFFF;
    border-radius: 3px;
}

QTabBar::tab {
    background-color: #F4F5F7;
    color: #444444;
    min-width: 100px;
    padding: 8px 15px;
    border: 1px solid #D2D6DE;
    border-bottom: none;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    border-top: 2px solid #3C8DBC;
}

/* スクロールバー */
QScrollBar:vertical {
    background-color: #F4F5F7;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #D2D6DE;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""
