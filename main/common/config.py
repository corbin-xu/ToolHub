"""应用配置的读取与保存。"""

import json
import os
import sys
from pathlib import Path


def _config_path():
    """安装包运行时 config 与 exe 同目录；开发时为当前工作目录下的 config.json。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "config.json"
    return Path("config.json")


class ConfigManager:
    """配置管理器"""
    
    CONFIG_FILE = "config.json"  # 仅作默认名，实际路径用 _config_path()
    
    DEFAULT_CONFIG = {
        'ignored_versions': [],           # 用户选择“忽略该版本”的版本号列表
    }
    
    def __init__(self):
        self.config = self.load_config()
    
    @staticmethod
    def load_config() -> dict:
        """加载配置文件"""
        path = _config_path()
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置和加载的配置
                    return {**ConfigManager.DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"配置加载失败: {e}，使用默认配置")
                return ConfigManager.DEFAULT_CONFIG.copy()
        return ConfigManager.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(_config_path(), 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"配置保存失败: {e}")
            return False
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """设置配置值"""
        self.config[key] = value
