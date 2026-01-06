"""
数据处理模块 - 处理关键词报表导入、验证、清洗等
"""

import csv
import json
from typing import List, Dict, Tuple
from datetime import datetime


class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def load_keyword_report(file_path: str) -> Tuple[List[Dict], List[str]]:
        """
        从 CSV 关键词报表加载数据
        
        Returns:
            (数据列表, 错误列表)
        """
        data = []
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    errors.append("CSV 文件为空或格式错误")
                    return data, errors
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # 转换数值字段
                        processed_row = {}
                        for key, value in row.items():
                            if key in ['展现数', '点击数', '总订单行', '间接订单行', '直接订单行', '预售订单行']:
                                processed_row[key] = int(value) if value else 0
                            elif key in ['花费', '千次展现成本', '平均点击成本', '直接订单金额', 
                                        '间接订单金额', '总订单金额', '预售订单金额', '加购成本', '平均订单成本']:
                                processed_row[key] = float(value) if value else 0.0
                            elif key in ['点击率(%)', '加购率(%)', '转化率(%)']:
                                processed_row[key] = float(value) if value else 0.0
                            else:
                                processed_row[key] = value
                        
                        # 过滤掉展现数为0的记录
                        if processed_row.get('展现数', 0) > 0:
                            data.append(processed_row)
                    except Exception as e:
                        errors.append(f"第 {row_num} 行处理失败: {str(e)}")
        
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    reader = csv.DictReader(f)
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            processed_row = {}
                            for key, value in row.items():
                                if key in ['展现数', '点击数', '总订单行', '间接订单行', '直接订单行', '预售订单行']:
                                    processed_row[key] = int(value) if value else 0
                                elif key in ['花费', '千次展现成本', '平均点击成本', '直接订单金额', 
                                            '间接订单金额', '总订单金额', '预售订单金额', '加购成本', '平均订单成本']:
                                    processed_row[key] = float(value) if value else 0.0
                                elif key in ['点击率(%)', '加购率(%)', '转化率(%)']:
                                    processed_row[key] = float(value) if value else 0.0
                                else:
                                    processed_row[key] = value
                            
                            if processed_row.get('展现数', 0) > 0:
                                data.append(processed_row)
                        except Exception as e:
                            errors.append(f"第 {row_num} 行处理失败: {str(e)}")
            except Exception as e:
                errors.append(f"CSV 文件读取失败 (尝试 GBK 编码): {e}")
        except Exception as e:
            errors.append(f"CSV 文件读取失败: {e}")
        
        return data, errors
    
    @staticmethod
    def export_to_csv(data: List[Dict], file_path: str) -> bool:
        """导出分析结果到 CSV 文件"""
        try:
            if not data:
                print("没有数据可导出")
                return False
            
            fieldnames = list(data[0].keys())
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    @staticmethod
    def filter_by_strategy(data: List[Dict], strategy: str) -> List[Dict]:
        """按优化策略筛选关键词"""
        return [r for r in data if r.get('优化策略', '') == strategy]
    
    @staticmethod
    def filter_by_impression_range(data: List[Dict], min_imp: int, max_imp: int) -> List[Dict]:
        """按展现数范围筛选"""
        return [r for r in data if min_imp <= r.get('展现数', 0) <= max_imp]
    
    @staticmethod
    def filter_by_cost_range(data: List[Dict], min_cost: float, max_cost: float) -> List[Dict]:
        """按花费范围筛选"""
        return [r for r in data if min_cost <= r.get('花费', 0) <= max_cost]
    
    @staticmethod
    def sort_by_field(data: List[Dict], field: str, reverse: bool = True) -> List[Dict]:
        """按指定字段排序"""
        try:
            return sorted(data, key=lambda x: x.get(field, 0), reverse=reverse)
        except:
            return data
