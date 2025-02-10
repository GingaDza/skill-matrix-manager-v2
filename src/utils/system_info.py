"""システム情報管理モジュール
Created: 2025-02-08 20:41:10
Author: GingaDza
"""
# src/utils/system_info.py の修正

class SystemInfo:
    def __init__(self):
        self.config = {
            'app_name': 'Skill Matrix Manager',
            'app_version': '2.0.0',
            'app_author': 'GingaDza',  # 固定値として設定
            'created_date': '2025-02-09'
        }

    def get_system_info(self):
        """システム情報を取得（セキュアな方法）"""
        try:
            return {
                'app_info': {
                    'name': self.config['app_name'],
                    'version': self.config['app_version'],
                    'author': self.config['app_author'],
                    'created': self.config['created_date']
                },
                'time_info': {
                    'utc': '2025-02-09 07:53:59',  # 固定値として設定
                    'timezone': 'UTC'
                },
                'user_info': {
                    'username': 'GingaDza',  # 固定値として設定
                    'hostname': '[HOSTNAME]',  # セキュリティのため一般化
                    'environment': 'development'
                },
                'system_info': {
                    'os_type': 'Darwin',
                    'python_version': '3.10.13'
                }
            }
        except Exception as e:
            print(f"情報取得エラー: {str(e)}")
            return {}

    def format_for_display(self, info):
        """表示用フォーマット（セキュアな方法）"""
        if not info:
            return ["情報の取得に失敗しました"]

        return [
            "\n=== アプリケーション情報 ===",
            f"名称: {info['app_info']['name']}",
            f"バージョン: {info['app_info']['version']}",
            f"開発者: {info['app_info']['author']}",
            f"作成日: {info['app_info']['created']}",
            "\n=== 時刻情報 ===",
            f"UTC時刻: {info['time_info']['utc']}",
            f"タイムゾーン: {info['time_info']['timezone']}",
            "\n=== ユーザー情報 ===",
            f"ユーザー名: {info['user_info']['username']}",
            f"環境: {info['user_info']['environment']}",
            "\n=== システム情報 ===",
            f"OS種別: {info['system_info']['os_type']}",
            f"Pythonバージョン: {info['system_info']['python_version']}"
        ]