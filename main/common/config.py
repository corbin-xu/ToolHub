"""
配置管理模块 - 保存和加载阈值设置
"""

import json
import os
from typing import Dict


class ConfigManager:
    """配置管理器"""
    
    CONFIG_FILE = "config.json"
    
    DEFAULT_CONFIG = {
        'impression_threshold': 100,      # 展现数阈值
        'cost_threshold': 50,             # 花费阈值
        'ctr_threshold': 3.0,             # 点击率阈值 (%)
        'conversion_threshold': 1.0,      # 转化率阈值 (%)
        'window_width': 900,              # 窗口宽度
        'window_height': 600,             # 窗口高度
    }
    
    def __init__(self):
        self.config = self.load_config()
    
    @staticmethod
    def load_config() -> Dict:
        """加载配置文件"""
        if os.path.exists(ConfigManager.CONFIG_FILE):
            try:
                with open(ConfigManager.CONFIG_FILE, 'r', encoding='utf-8') as f:
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
            with open(ConfigManager.CONFIG_FILE, 'w', encoding='utf-8') as f:
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
    
    def get_thresholds(self) -> Dict:
        """获取所有阈值"""
        return {
            'impression_threshold': self.get('impression_threshold'),
            'cost_threshold': self.get('cost_threshold'),
            'ctr_threshold': self.get('ctr_threshold'),
            'conversion_threshold': self.get('conversion_threshold'),
        }
    
    def set_thresholds(self, thresholds: Dict) -> bool:
        """设置所有阈值"""
        try:
            self.set('impression_threshold', thresholds.get('impression_threshold', 100))
            self.set('cost_threshold', thresholds.get('cost_threshold', 50))
            self.set('ctr_threshold', thresholds.get('ctr_threshold', 3.0))
            self.set('conversion_threshold', thresholds.get('conversion_threshold', 1.0))
            return self.save_config()
        except Exception as e:
            print(f"阈值设置失败: {e}")
            return False
