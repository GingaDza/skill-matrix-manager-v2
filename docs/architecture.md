# アーキテクチャ設計

## プロジェクト構造
- src/: ソースコード
  - database/: データベース管理
  - models/: データモデル
  - utils/: ユーティリティ
  - views/: UI実装
    - dialogs/: ダイアログ
    - tabs/: タブ実装
    - main_window.py: メインウィンドウ

## 設計方針
- MVCアーキテクチャの採用
- データベース層の分離
- モジュール化されたUI実装
