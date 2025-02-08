"""マイグレーション実行スクリプト
Created: 2025-02-08 14:09:30
Author: GingaDza
"""
import os
from pathlib import Path
from .database.migrations.migration_manager import MigrationManager
from .utils.logger import setup_logger
from .config import settings

def run_migrations():
    """マイグレーションの実行"""
    logger = setup_logger(__name__)
    db_path = os.path.join("data", settings.DATABASE["name"])
    
    # データディレクトリの作成
    Path("data").mkdir(exist_ok=True)
    
    manager = MigrationManager(db_path)
    applied = manager.get_applied_migrations()
    
    # V20250208140405__initial_schema.py のマイグレーションを実行
    from .database.migrations.V20250208140405__initial_schema import upgrade
    if "V20250208140405" not in applied:
        if manager.apply_migration("V20250208140405", upgrade):
            logger.info("初期スキーマのマイグレーションが完了しました")
        else:
            logger.error("初期スキーマのマイグレーションに失敗しました")

if __name__ == "__main__":
    run_migrations()
