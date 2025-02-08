"""ロギング設定"""
import logging
import sys
from datetime import datetime

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'app_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )
