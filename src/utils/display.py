"""表示管理クラス"""
import sys
from datetime import datetime
from typing import Optional

class DisplayManager:
    def __init__(self):
        self.colors = {
            'success': '\033[92m',  # 緑
            'error': '\033[91m',    # 赤
            'info': '\033[94m',     # 青
            'warning': '\033[93m',  # 黄
            'reset': '\033[0m'      # リセット
        }

    def show_app_info(self):
        """アプリケーション情報を表示"""
        self._print_header("Skill Matrix Manager")
        self._print_info("Version: 1.0.0")
        self._print_info(f"Start Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        self._print_separator()

    def show_message(self, message: str, type: str = 'info'):
        """メッセージを表示"""
        color = self.colors.get(type, self.colors['reset'])
        print(f"{color}{message}{self.colors['reset']}")

    def show_section(self, title: str):
        """セクションタイトルを表示"""
        self._print_separator()
        self._print_info(f"=== {title} ===")
        self._print_separator()

    def show_error(self, message: str, error: Optional[Exception] = None):
        """エラーメッセージを表示"""
        self.show_message(f"エラー: {message}", 'error')
        if error:
            self.show_message(f"詳細: {str(error)}", 'error')

    def _print_header(self, text: str):
        """ヘッダーを表示"""
        self._print_separator()
        self._print_centered(text)
        self._print_separator()

    def _print_info(self, text: str):
        """情報を表示"""
        print(f"{self.colors['info']}{text}{self.colors['reset']}")

    def _print_separator(self):
        """区切り線を表示"""
        print(f"{self.colors['info']}{'='*50}{self.colors['reset']}")

    def _print_centered(self, text: str):
        """中央揃えでテキストを表示"""
        width = 50
        padding = (width - len(text)) // 2
        print(f"{self.colors['info']}{' '*padding}{text}{self.colors['reset']}")

# DisplayManagerのインスタンスを作成
display = DisplayManager()

# モジュールとしてインポートされた場合に使用できるようにエクスポート
__all__ = ['display']
