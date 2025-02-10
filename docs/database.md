# データベース設計

## テーブル構造
1. users: ユーザー情報
2. groups: グループ情報
3. categories: カテゴリー情報
4. skills: スキル情報
5. evaluations: 評価情報

## リレーション
- users -> groups (多対1)
- skills -> categories (多対1)
- evaluations -> users, skills (多対多)
