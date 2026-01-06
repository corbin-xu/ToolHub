"""
电商投流优化分析工具 - 核心分析模块
支持关键词报表分析、优化建议生成等功能
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple
import statistics


class KeywordOptimizer:
    """关键词优化分析器"""
    
    # 优化建议规则表
    OPTIMIZATION_RULES = {
        ('小', '高', '高', '高'): {
            'strategy': '继续保持或适当加价',
            'reason': '行业展现量小，表现好可稳住或稍加价'
        },
        ('小', '高', '高', '低'): {
            'strategy': '先降价，看ROI',
            'reason': '花费高转化低，先调整出价对比ROI'
        },
        ('小', '高', '低', '高'): {
            'strategy': '优化图片/创意',
            'reason': '精准词，点击率低但转化高，图片创意可能问题'
        },
        ('小', '高', '低', '低'): {
            'strategy': '直接删除',
            'reason': '只花钱不产出，无效关键词'
        },
        ('小', '低', '高', '高'): {
            'strategy': '以ROI为重点加价',
            'reason': '高点击高转化，可加价获取更多流量'
        },
        ('小', '低', '高', '低'): {
            'strategy': '提价观察转化，仍低则删除',
            'reason': '高点击词可带流量，提价观察ROI'
        },
        ('小', '低', '低', '高'): {
            'strategy': '运气好',
            'reason': '长时间展现低，可考虑删除'
        },
        ('小', '低', '低', '低'): {
            'strategy': '适当加价+优化创意，效果差则删除',
            'reason': '展现量小参考意义低，先优化再考虑删除'
        },
        ('大', '高', '高', '高'): {
            'strategy': '继续保持，增加投放时间',
            'reason': '高转化词可降低PPC，继续投放即可'
        },
        ('大', '高', '高', '低'): {
            'strategy': '降价或删除',
            'reason': '高出价高展现但转化低，后期ROI低可删除'
        },
        ('大', '高', '低', '高'): {
            'strategy': '优化创意或适当提价，点击率仍低则删除',
            'reason': '点击率低需大量流量维持，影响计划权重'
        },
        ('大', '高', '低', '低'): {
            'strategy': '降价或删除',
            'reason': '类目大词，严重影响计划权重则删除'
        },
        ('大', '低', '高', '高'): {
            'strategy': '加价获取更多流量',
            'reason': '低出价高表现，可加价扩大规模'
        },
        ('大', '低', '高', '低'): {
            'strategy': '提价观察，转化仍低则删除',
            'reason': '高展现高点击但转化低，需观察ROI'
        },
        ('大', '低', '低', '高'): {
            'strategy': '优化创意+提价',
            'reason': '大词低点击但高转化，创意优化空间大'
        },
        ('大', '低', '低', '低'): {
            'strategy': '删除或大幅优化',
            'reason': '大词无效，严重浪费预算'
        },
    }
    
    def __init__(self, thresholds: Dict = None):
        self.data = []
        # 设置阈值
        self.impression_threshold = thresholds.get('impression_threshold', 100) if thresholds else 100
        self.cost_threshold = thresholds.get('cost_threshold', 50) if thresholds else 50
        self.ctr_threshold = thresholds.get('ctr_threshold', 3.0) if thresholds else 3.0
        self.conversion_threshold = thresholds.get('conversion_threshold', 1.0) if thresholds else 1.0
    
    def load_data(self, data_source: List[Dict]) -> bool:
        """加载关键词报表数据"""
        try:
            self.data = data_source
            return True
        except Exception as e:
            print(f"数据加载失败: {e}")
            return False
    
    def categorize_metric(self, value: float, metric_type: str) -> str:
        """
        将指标值分类为 '大' 或 '小'
        
        Args:
            value: 指标值
            metric_type: 指标类型 ('impression', 'cost', 'ctr', 'conversion')
        """
        if metric_type == 'impression':
            # 展现数：以设定阈值为界
            return '大' if value >= self.impression_threshold else '小'
        
        elif metric_type == 'cost':
            # 花费：以设定阈值为界
            return '高' if value >= self.cost_threshold else '低'
        
        elif metric_type == 'ctr':
            # 点击率：以设定阈值为界
            return '高' if value >= self.ctr_threshold else '低'
        
        elif metric_type == 'conversion':
            # 转化率：以设定阈值为界
            return '高' if value >= self.conversion_threshold else '低'
        
        return '未知'
    
    def get_optimization_suggestion(self, keyword_data: Dict) -> Dict:
        """获取关键词的优化建议"""
        impression_cat = self.categorize_metric(keyword_data.get('展现数', 0), 'impression')
        cost_cat = self.categorize_metric(keyword_data.get('花费', 0), 'cost')
        ctr_cat = self.categorize_metric(keyword_data.get('点击率(%)', 0), 'ctr')
        conversion_cat = self.categorize_metric(keyword_data.get('转化率(%)', 0), 'conversion')
        
        rule_key = (impression_cat, cost_cat, ctr_cat, conversion_cat)
        rule = self.OPTIMIZATION_RULES.get(rule_key, {
            'strategy': '需要人工评估',
            'reason': '未知组合'
        })
        
        return {
            '展现量': impression_cat,
            '出价': cost_cat,
            '点击率': ctr_cat,
            '转化率': conversion_cat,
            '优化策略': rule['strategy'],
            '原因说明': rule['reason']
        }
    
    def analyze_all_keywords(self) -> List[Dict]:
        """分析所有关键词并生成优化建议"""
        results = []
        for keyword_data in self.data:
            suggestion = self.get_optimization_suggestion(keyword_data)
            results.append({
                '关键词': keyword_data.get('关键词', ''),
                '推广计划': keyword_data.get('推广计划', ''),
                '展现数': keyword_data.get('展现数', 0),
                '花费': keyword_data.get('花费', 0),
                '点击率(%)': keyword_data.get('点击率(%)', 0),
                '转化率(%)': keyword_data.get('转化率(%)', 0),
                '点击数': keyword_data.get('点击数', 0),
                '总订单行': keyword_data.get('总订单行', 0),
                '总订单金额': keyword_data.get('总订单金额', 0),
                **suggestion
            })
        return results
    
    def get_statistics(self) -> Dict:
        """获取整体统计信息"""
        if not self.data:
            return {}
        
        total_impression = sum(r.get('展现数', 0) for r in self.data)
        total_cost = sum(r.get('花费', 0) for r in self.data)
        total_clicks = sum(r.get('点击数', 0) for r in self.data)
        total_orders = sum(r.get('总订单行', 0) for r in self.data)
        total_revenue = sum(r.get('总订单金额', 0) for r in self.data)
        
        avg_ctr = (total_clicks / total_impression * 100) if total_impression > 0 else 0
        avg_conversion = (total_orders / total_clicks * 100) if total_clicks > 0 else 0
        roi = (total_revenue / total_cost) if total_cost > 0 else 0
        
        return {
            '关键词总数': len(self.data),
            '总展现数': total_impression,
            '总点击数': total_clicks,
            '总花费': total_cost,
            '总订单数': total_orders,
            '总订单金额': total_revenue,
            '平均点击率(%)': avg_ctr,
            '平均转化率(%)': avg_conversion,
            '投产比': roi,
            '平均单次点击成本': total_cost / total_clicks if total_clicks > 0 else 0
        }
    
    def get_recommended_thresholds(self) -> Dict:
        """计算推荐的阈值（基于数据的中位数）"""
        if not self.data:
            return {}
        
        impressions = [r.get('展现数', 0) for r in self.data if r.get('展现数', 0) > 0]
        costs = [r.get('花费', 0) for r in self.data if r.get('花费', 0) > 0]
        ctrs = [r.get('点击率(%)', 0) for r in self.data if r.get('点击率(%)', 0) > 0]
        conversions = [r.get('转化率(%)', 0) for r in self.data if r.get('转化率(%)', 0) > 0]
        
        return {
            'impression_threshold': int(statistics.median(impressions)) if impressions else 100,
            'cost_threshold': round(statistics.median(costs), 2) if costs else 50,
            'ctr_threshold': round(statistics.median(ctrs), 2) if ctrs else 3.0,
            'conversion_threshold': round(statistics.median(conversions), 2) if conversions else 1.0,
        }
    
    def generate_report(self) -> str:
        """生成完整分析报告"""
        report = []
        report.append("=" * 80)
        report.append("电商投流优化分析报告")
        report.append("=" * 80)
        report.append("")
        
        # 整体统计
        stats = self.get_statistics()
        report.append("【整体统计】")
        for key, value in stats.items():
            if isinstance(value, float):
                report.append(f"  {key}: {value:.2f}")
            else:
                report.append(f"  {key}: {value}")
        report.append("")
        
        # 关键词优化建议
        report.append("【关键词优化建议】")
        suggestions = self.analyze_all_keywords()
        
        # 按优化策略分类
        strategy_groups = {}
        for item in suggestions:
            strategy = item['优化策略']
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(item)
        
        for strategy, keywords in strategy_groups.items():
            report.append(f"\n  {strategy} ({len(keywords)}个关键词):")
            for kw in keywords[:5]:  # 每个策略显示前5个
                report.append(f"    - {kw['关键词']}: 展现{kw['展现数']}, 花费¥{kw['花费']:.2f}, 点击率{kw['点击率(%)']:.2f}%, 转化率{kw['转化率(%)']:.2f}%")
            if len(keywords) > 5:
                report.append(f"    ... 还有 {len(keywords) - 5} 个关键词")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def get_keywords_by_plan(self) -> Dict[str, List[Dict]]:
        """按推广计划分组关键词"""
        plan_groups = {}
        for keyword in self.current_keywords if hasattr(self, 'current_keywords') else self.analyze_all_keywords():
            plan = keyword.get('推广计划', '未分类')
            if plan not in plan_groups:
                plan_groups[plan] = []
            plan_groups[plan].append(keyword)
        return plan_groups
