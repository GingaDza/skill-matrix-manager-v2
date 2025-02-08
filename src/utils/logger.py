"""ロガー設定モジュール
Created: 2025-02-08 20:44:07
Author: GingaDza
"""
import logging
import sys
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """ロガーのセットアップ"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # ファイルハンドラ
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "app.log", encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        # コンソールハンドラ
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger
