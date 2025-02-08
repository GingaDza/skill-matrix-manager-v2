"""システム情報管理モジュール
Created: 2025-02-08 20:41:10
Author: GingaDza
"""
class SystemInfo:
    def __init__(self):
        self._app_version = "2.0.0"
        self._current_user = "GingaDza"
        self._current_time = "2025-02-08 20:41:10"

    @property
    def app_version(self) -> str:
        return self._app_version

    @property
    def current_user(self) -> str:
        return self._current_user

    @property
    def current_time(self) -> str:
        return self._current_time

    def get_system_status(self) -> dict:
        return {
            "database": {
                "name": "skill_matrix.db",
                "version": "2.0.0"
            },
            "logging": {
                "version": "1.0.0",
                "handlers": {
                    "file": {"level": "INFO"},
                    "console": {"level": "DEBUG"}
                }
            }
        }
