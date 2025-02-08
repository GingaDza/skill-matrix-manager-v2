"""アプリケーション設定
Created: 2025-02-08 13:52:49
Author: GingaDza
"""

# アプリケーション基本設定
APP_NAME = "Skill Matrix Manager"
APP_VERSION = "2.0.0"
CURRENT_USER = "GingaDza"
CURRENT_TIME = "2025-02-08 13:52:49"

# データベース設定
DATABASE = {
    "name": "skill_matrix.db",
    "version": "1.0.0",
    "created_at": "2025-02-08 13:52:49",
    "created_by": "GingaDza"
}

# ログ設定
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "level": "DEBUG"
        }
    }
}
