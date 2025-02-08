"""ベースデータベース管理クラス
Created: 2025-02-08 20:44:07
Author: GingaDza
"""
import sqlite3
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
from ..utils.logger import setup_logger

class BaseManager:
    """基本データベース管理クラス"""

    def __init__(self, db_path: str = "data/skill_matrix.db"):
        self.logger = setup_logger(__name__)
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()

    def _ensure_data_directory(self):
        """データディレクトリの確保"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """データベースの初期化"""
        with self.get_connection() as conn:
            conn.executescript(self.get_init_sql())

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """データベース接続を取得"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        finally:
            if conn:
                conn.close()

    def get_init_sql(self) -> str:
        """初期化用SQLの取得"""
        return ""
