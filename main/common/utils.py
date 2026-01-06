"""
工具函数模块
"""

from typing import List, Dict
from datetime import datetime


def format_currency(amount: float) -> str:
    """格式化货币显示"""
    return f"¥{amount:,.2f}"


def format_percentage(value: float, total: float) -> str:
    """格式化百分比"""
    if total == 0:
        return "0.00%"
    return f"{(value / total * 100):.2f}%"


def parse_timestamp(timestamp_str: str) -> datetime:
    """解析时间戳字符串"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"无法解析时间戳: {timestamp_str}")


def print_table(headers: List[str], rows: List[List], col_widths: List[int] = None) -> str:
    """生成表格字符串"""
    if not col_widths:
        col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    
    lines = []
    
    # 表头
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    # 数据行
    for row in rows:
        row_line = " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row))
        lines.append(row_line)
    
    return "\n".join(lines)


def get_date_range_summary(data: List[Dict]) -> Dict:
    """获取数据的日期范围摘要"""
    if not data:
        return {'start_date': None, 'end_date': None, 'days': 0}
    
    dates = sorted([r.get('timestamp', '').split(' ')[0] for r in data])
    
    return {
        'start_date': dates[0],
        'end_date': dates[-1],
        'days': len(set(dates))
    }
