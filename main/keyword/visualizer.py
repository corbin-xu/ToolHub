"""
可视化模块 - 生成表格和图表展示
"""

from typing import List, Dict
from main.common.utils import format_currency


class Visualizer:
    """可视化工具"""
    
    @staticmethod
    def print_keyword_table(keywords: List[Dict], max_rows: int = None) -> str:
        """
        生成关键词分析表格
        
        Args:
            keywords: 关键词数据列表
            max_rows: 最多显示行数
        """
        if not keywords:
            return "没有数据"
        
        # 限制显示行数
        display_data = keywords[:max_rows] if max_rows else keywords
        
        lines = []
        lines.append("")
        lines.append("┌" + "─" * 150 + "┐")
        
        # 表头
        header = "│ {:<15} │ {:<10} │ {:<10} │ {:<10} │ {:<10} │ {:<15} │ {:<20} │ {:<30} │".format(
            "关键词", "展现数", "花费(¥)", "点击率(%)", "转化率(%)", "订单数", "订单金额(¥)", "优化策略"
        )
        lines.append(header)
        lines.append("├" + "─" * 150 + "┤")
        
        # 数据行
        for item in display_data:
            row = "│ {:<15} │ {:<10} │ {:<10} │ {:<10} │ {:<10} │ {:<15} │ {:<20} │ {:<30} │".format(
                item.get('关键词', '')[:15],
                str(item.get('展现数', 0)),
                f"{item.get('花费', 0):.2f}",
                f"{item.get('点击率(%)', 0):.2f}",
                f"{item.get('转化率(%)', 0):.2f}",
                str(item.get('总订单行', 0)),
                f"{item.get('总订单金额', 0):.2f}",
                item.get('优化策略', '')[:30]
            )
            lines.append(row)
        
        lines.append("└" + "─" * 150 + "┘")
        
        if max_rows and len(keywords) > max_rows:
            lines.append(f"... 还有 {len(keywords) - max_rows} 个关键词")
        
        return "\n".join(lines)
    
    @staticmethod
    def print_strategy_summary(keywords: List[Dict]) -> str:
        """生成优化策略汇总表"""
        if not keywords:
            return "没有数据"
        
        # 按策略分组
        strategy_groups = {}
        for item in keywords:
            strategy = item.get('优化策略', '未知')
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(item)
        
        lines = []
        lines.append("")
        lines.append("=" * 80)
        lines.append("优化策略汇总")
        lines.append("=" * 80)
        
        for strategy, items in sorted(strategy_groups.items(), key=lambda x: len(x[1]), reverse=True):
            total_cost = sum(item.get('花费', 0) for item in items)
            total_revenue = sum(item.get('总订单金额', 0) for item in items)
            roi = (total_revenue / total_cost) if total_cost > 0 else 0
            
            lines.append(f"\n【{strategy}】({len(items)}个关键词)")
            lines.append(f"  总花费: ¥{total_cost:.2f}")
            lines.append(f"  总订单金额: ¥{total_revenue:.2f}")
            lines.append(f"  投产比: {roi:.2f}")
            
            # 显示前3个关键词
            for i, item in enumerate(items[:3], 1):
                lines.append(f"  {i}. {item.get('关键词', '')} - 展现{item.get('展现数', 0)}, 花费¥{item.get('花费', 0):.2f}, 转化率{item.get('转化率(%)', 0):.2f}%")
            
            if len(items) > 3:
                lines.append(f"  ... 还有 {len(items) - 3} 个关键词")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
    
    @staticmethod
    def print_performance_chart(keywords: List[Dict]) -> str:
        """生成性能对比图表"""
        if not keywords:
            return "没有数据"
        
        lines = []
        lines.append("")
        lines.append("=" * 80)
        lines.append("关键词性能对比")
        lines.append("=" * 80)
        
        # 按展现数排序，显示前10个
        top_keywords = sorted(keywords, key=lambda x: x.get('展现数', 0), reverse=True)[:10]
        
        lines.append("\n【展现数 TOP 10】")
        for i, item in enumerate(top_keywords, 1):
            impression = item.get('展现数', 0)
            bar_length = min(impression // 100, 50)
            bar = "█" * bar_length
            lines.append(f"  {i:2}. {item.get('关键词', ''):<15} {bar} {impression}")
        
        # 按花费排序
        top_cost = sorted(keywords, key=lambda x: x.get('花费', 0), reverse=True)[:10]
        lines.append("\n【花费 TOP 10】")
        for i, item in enumerate(top_cost, 1):
            cost = item.get('花费', 0)
            bar_length = min(int(cost / 5), 50)
            bar = "█" * bar_length
            lines.append(f"  {i:2}. {item.get('关键词', ''):<15} {bar} ¥{cost:.2f}")
        
        # 按转化率排序
        top_conversion = sorted(keywords, key=lambda x: x.get('转化率(%)', 0), reverse=True)[:10]
        lines.append("\n【转化率 TOP 10】")
        for i, item in enumerate(top_conversion, 1):
            conversion = item.get('转化率(%)', 0)
            bar_length = min(int(conversion * 5), 50)
            bar = "█" * bar_length
            lines.append(f"  {i:2}. {item.get('关键词', ''):<15} {bar} {conversion:.2f}%")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
    
    @staticmethod
    def print_detailed_analysis(keyword_data: Dict) -> str:
        """生成单个关键词的详细分析"""
        lines = []
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"关键词详细分析: {keyword_data.get('关键词', '')}")
        lines.append("=" * 60)
        
        lines.append("\n【基础数据】")
        lines.append(f"  展现数: {keyword_data.get('展现数', 0)}")
        lines.append(f"  点击数: {keyword_data.get('点击数', 0)}")
        lines.append(f"  花费: ¥{keyword_data.get('花费', 0):.2f}")
        lines.append(f"  点击率: {keyword_data.get('点击率(%)', 0):.2f}%")
        lines.append(f"  转化率: {keyword_data.get('转化率(%)', 0):.2f}%")
        
        lines.append("\n【成本指标】")
        lines.append(f"  千次展现成本: ¥{keyword_data.get('千次展现成本', 0):.2f}")
        lines.append(f"  平均点击成本: ¥{keyword_data.get('平均点击成本', 0):.2f}")
        lines.append(f"  平均订单成本: ¥{keyword_data.get('平均订单成本', 0):.2f}")
        
        lines.append("\n【转化数据】")
        lines.append(f"  直接订单: {keyword_data.get('直接订单行', 0)} 单，¥{keyword_data.get('直接订单金额', 0):.2f}")
        lines.append(f"  间接订单: {keyword_data.get('间接订单行', 0)} 单，¥{keyword_data.get('间接订单金额', 0):.2f}")
        lines.append(f"  总订单: {keyword_data.get('总订单行', 0)} 单，¥{keyword_data.get('总订单金额', 0):.2f}")
        
        lines.append("\n【加购数据】")
        lines.append(f"  总加购数: {keyword_data.get('总加购数', 0)}")
        lines.append(f"  加购率: {keyword_data.get('加购率(%)', 0):.2f}%")
        lines.append(f"  加购成本: ¥{keyword_data.get('加购成本', 0):.2f}")
        
        lines.append("\n【优化建议】")
        lines.append(f"  展现量: {keyword_data.get('展现量', '')}")
        lines.append(f"  出价: {keyword_data.get('出价', '')}")
        lines.append(f"  点击率: {keyword_data.get('点击率', '')}")
        lines.append(f"  转化率: {keyword_data.get('转化率', '')}")
        lines.append(f"  优化策略: {keyword_data.get('优化策略', '')}")
        lines.append(f"  原因说明: {keyword_data.get('原因说明', '')}")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
