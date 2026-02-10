#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
箱唛生成工具 - 基于模板的箱唛文件生成
"""

import os
import sys
import shutil
import re
from pathlib import Path


def _get_app_base_dir() -> Path:
    """应用根目录：安装包运行时为 exe 所在目录，否则为项目根目录（main/label 的上级两级）。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.resolve()
    return Path(__file__).parent.parent.parent.resolve()


class CartonMarkGenerator:
    """箱唛生成器"""
    
    # 城市映射
    CITY_OPTIONS = {
        "1": {"city": "北京市", "label": "北京"},
        "2": {"city": "上海市", "label": "上海"},
        "3": {"city": "广东省 广州市", "label": "广州"},
        "4": {"city": "四川省 成都市", "label": "成都"},
        "5": {"city": "湖北省 武汉市", "label": "武汉"},
        "6": {"city": "辽宁省 沈阳市", "label": "沈阳"},
        "7": {"city": "陕西省 西安市", "label": "西安"},
        "8": {"city": "山东省 德州市", "label": "德州"}
    }
    # 城市到所属省份映射（可按需继续补充，至少覆盖常用城市）
    CITY_PROVINCE_MAP = {
        # 直辖市 / 特别行政区
        "北京": "北京",
        "上海": "上海",
        "天津": "天津",
        "重庆": "重庆",
        "香港": "香港",
        "澳门": "澳门",
        # 华北
        "石家庄": "河北",
        "唐山": "河北",
        "秦皇岛": "河北",
        "邯郸": "河北",
        "邢台": "河北",
        "保定": "河北",
        "张家口": "河北",
        "承德": "河北",
        "沧州": "河北",
        "廊坊": "河北",
        "衡水": "河北",
        "太原": "山西",
        "大同": "山西",
        "阳泉": "山西",
        "长治": "山西",
        "晋城": "山西",
        "朔州": "山西",
        "晋中": "山西",
        "运城": "山西",
        "忻州": "山西",
        "临汾": "山西",
        "吕梁": "山西",
        "呼和浩特": "内蒙古",
        "包头": "内蒙古",
        "乌海": "内蒙古",
        "赤峰": "内蒙古",
        "通辽": "内蒙古",
        "鄂尔多斯": "内蒙古",
        "呼伦贝尔": "内蒙古",
        "巴彦淖尔": "内蒙古",
        "乌兰察布": "内蒙古",
        "兴安盟": "内蒙古",
        "锡林郭勒盟": "内蒙古",
        "阿拉善盟": "内蒙古",
        # 东北
        "沈阳": "辽宁",
        "大连": "辽宁",
        "鞍山": "辽宁",
        "抚顺": "辽宁",
        "本溪": "辽宁",
        "丹东": "辽宁",
        "锦州": "辽宁",
        "营口": "辽宁",
        "阜新": "辽宁",
        "辽阳": "辽宁",
        "盘锦": "辽宁",
        "铁岭": "辽宁",
        "朝阳": "辽宁",
        "葫芦岛": "辽宁",
        "长春": "吉林",
        "吉林": "吉林",
        "四平": "吉林",
        "辽源": "吉林",
        "通化": "吉林",
        "白山": "吉林",
        "松原": "吉林",
        "白城": "吉林",
        "延边": "吉林",
        "哈尔滨": "黑龙江",
        "齐齐哈尔": "黑龙江",
        "鸡西": "黑龙江",
        "鹤岗": "黑龙江",
        "双鸭山": "黑龙江",
        "大庆": "黑龙江",
        "伊春": "黑龙江",
        "佳木斯": "黑龙江",
        "七台河": "黑龙江",
        "牡丹江": "黑龙江",
        "黑河": "黑龙江",
        "绥化": "黑龙江",
        "大兴安岭": "黑龙江",
        # 华东
        "南京": "江苏",
        "无锡": "江苏",
        "徐州": "江苏",
        "常州": "江苏",
        "苏州": "江苏",
        "南通": "江苏",
        "连云港": "江苏",
        "淮安": "江苏",
        "盐城": "江苏",
        "扬州": "江苏",
        "镇江": "江苏",
        "泰州": "江苏",
        "宿迁": "江苏",
        "杭州": "浙江",
        "宁波": "浙江",
        "温州": "浙江",
        "嘉兴": "浙江",
        "湖州": "浙江",
        "绍兴": "浙江",
        "金华": "浙江",
        "衢州": "浙江",
        "舟山": "浙江",
        "台州": "浙江",
        "丽水": "浙江",
        "合肥": "安徽",
        "芜湖": "安徽",
        "蚌埠": "安徽",
        "淮南": "安徽",
        "马鞍山": "安徽",
        "淮北": "安徽",
        "铜陵": "安徽",
        "安庆": "安徽",
        "黄山": "安徽",
        "滁州": "安徽",
        "阜阳": "安徽",
        "宿州": "安徽",
        "六安": "安徽",
        "亳州": "安徽",
        "池州": "安徽",
        "宣城": "安徽",
        "福州": "福建",
        "厦门": "福建",
        "莆田": "福建",
        "三明": "福建",
        "泉州": "福建",
        "漳州": "福建",
        "南平": "福建",
        "龙岩": "福建",
        "宁德": "福建",
        "南昌": "江西",
        "景德镇": "江西",
        "萍乡": "江西",
        "九江": "江西",
        "新余": "江西",
        "鹰潭": "江西",
        "赣州": "江西",
        "吉安": "江西",
        "宜春": "江西",
        "抚州": "江西",
        "上饶": "江西",
        "济南": "山东",
        "青岛": "山东",
        "淄博": "山东",
        "枣庄": "山东",
        "东营": "山东",
        "烟台": "山东",
        "潍坊": "山东",
        "济宁": "山东",
        "泰安": "山东",
        "威海": "山东",
        "日照": "山东",
        "临沂": "山东",
        "德州": "山东",
        "聊城": "山东",
        "滨州": "山东",
        "菏泽": "山东",
        # 华中
        "郑州": "河南",
        "开封": "河南",
        "洛阳": "河南",
        "平顶山": "河南",
        "安阳": "河南",
        "鹤壁": "河南",
        "新乡": "河南",
        "焦作": "河南",
        "濮阳": "河南",
        "许昌": "河南",
        "漯河": "河南",
        "三门峡": "河南",
        "南阳": "河南",
        "商丘": "河南",
        "信阳": "河南",
        "周口": "河南",
        "驻马店": "河南",
        "济源": "河南",
        "武汉": "湖北",
        "黄石": "湖北",
        "十堰": "湖北",
        "宜昌": "湖北",
        "襄阳": "湖北",
        "鄂州": "湖北",
        "荆门": "湖北",
        "孝感": "湖北",
        "荆州": "湖北",
        "黄冈": "湖北",
        "咸宁": "湖北",
        "随州": "湖北",
        "恩施": "湖北",
        "长沙": "湖南",
        "株洲": "湖南",
        "湘潭": "湖南",
        "衡阳": "湖南",
        "邵阳": "湖南",
        "岳阳": "湖南",
        "常德": "湖南",
        "张家界": "湖南",
        "益阳": "湖南",
        "郴州": "湖南",
        "永州": "湖南",
        "怀化": "湖南",
        "娄底": "湖南",
        "湘西": "湖南",
        # 华南
        "广州": "广东",
        "韶关": "广东",
        "深圳": "广东",
        "珠海": "广东",
        "汕头": "广东",
        "佛山": "广东",
        "江门": "广东",
        "湛江": "广东",
        "茂名": "广东",
        "肇庆": "广东",
        "惠州": "广东",
        "梅州": "广东",
        "汕尾": "广东",
        "河源": "广东",
        "阳江": "广东",
        "清远": "广东",
        "东莞": "广东",
        "中山": "广东",
        "潮州": "广东",
        "揭阳": "广东",
        "云浮": "广东",
        "南宁": "广西",
        "柳州": "广西",
        "桂林": "广西",
        "梧州": "广西",
        "北海": "广西",
        "防城港": "广西",
        "钦州": "广西",
        "贵港": "广西",
        "玉林": "广西",
        "百色": "广西",
        "贺州": "广西",
        "河池": "广西",
        "来宾": "广西",
        "崇左": "广西",
        "海口": "海南",
        "三亚": "海南",
        "三沙": "海南",
        "儋州": "海南",
        # 西南
        "成都": "四川",
        "自贡": "四川",
        "攀枝花": "四川",
        "泸州": "四川",
        "德阳": "四川",
        "绵阳": "四川",
        "广元": "四川",
        "遂宁": "四川",
        "内江": "四川",
        "乐山": "四川",
        "南充": "四川",
        "眉山": "四川",
        "宜宾": "四川",
        "广安": "四川",
        "达州": "四川",
        "雅安": "四川",
        "巴中": "四川",
        "资阳": "四川",
        "贵阳": "贵州",
        "六盘水": "贵州",
        "遵义": "贵州",
        "安顺": "贵州",
        "黔西南": "贵州",
        "黔东南": "贵州",
        "黔南": "贵州",
        "昆明": "云南",
        "曲靖": "云南",
        "玉溪": "云南",
        "保山": "云南",
        "昭通": "云南",
        "丽江": "云南",
        "普洱": "云南",
        "临沧": "云南",
        "楚雄": "云南",
        "红河": "云南",
        "文山": "云南",
        "西双版纳": "云南",
        "大理": "云南",
        "德宏": "云南",
        "怒江": "云南",
        "迪庆": "云南",
        "拉萨": "西藏",
        "日喀则": "西藏",
        "昌都": "西藏",
        "林芝": "西藏",
        "山南": "西藏",
        "那曲": "西藏",
        "阿里": "西藏",
        # 西北
        "西安": "陕西",
        "铜川": "陕西",
        "宝鸡": "陕西",
        "咸阳": "陕西",
        "渭南": "陕西",
        "延安": "陕西",
        "汉中": "陕西",
        "榆林": "陕西",
        "安康": "陕西",
        "商洛": "陕西",
        "兰州": "甘肃",
        "嘉峪关": "甘肃",
        "金昌": "甘肃",
        "白银": "甘肃",
        "天水": "甘肃",
        "武威": "甘肃",
        "张掖": "甘肃",
        "平凉": "甘肃",
        "酒泉": "甘肃",
        "庆阳": "甘肃",
        "定西": "甘肃",
        "陇南": "甘肃",
        "临夏": "甘肃",
        "甘南": "甘肃",
        "西宁": "青海",
        "海东": "青海",
        "海北": "青海",
        "黄南": "青海",
        "海南": "青海",
        "果洛": "青海",
        "玉树": "青海",
        "海西": "青海",
        "银川": "宁夏",
        "石嘴山": "宁夏",
        "吴忠": "宁夏",
        "固原": "宁夏",
        "中卫": "宁夏",
        "乌鲁木齐": "新疆",
        "克拉玛依": "新疆",
        "吐鲁番": "新疆",
        "哈密": "新疆",
        "昌吉": "新疆",
        "博尔塔拉": "新疆",
        "巴音郭楞": "新疆",
        "阿克苏": "新疆",
        "克孜勒苏": "新疆",
        "喀什": "新疆",
        "和田": "新疆",
        "伊犁": "新疆",
        "塔城": "新疆",
        "阿勒泰": "新疆",
    }
    
    def __init__(self, template_path: str = None):
        """初始化箱唛生成器"""
        if template_path is None:
            base_dir = _get_app_base_dir()
            template_path = base_dir / "templates" / "carton_mark.pld"
        
        self.template_path = str(template_path)
        self.content = None

    @staticmethod
    def _format_destination_city(city_full: str, city_label: str, city_raw: str = None) -> str:
        """
        根据配置的城市全称和原始城市字段，生成箱唛中的“目的城市”展示文案。

        规则：
        1. 去掉“省”“市”等后缀；
        2. 如果有省 + 市（例如“广东省 广州市”、“陕西省 西安市”），显示为“广东 广州”、“陕西 西安”；
        3. 如果 Excel / 原始城市字段里带有数字后缀（如“北京2”、“西安114514”），
           则把数字后缀追加到最终结果上，比如“北京2”、“陕西 西安114514”。
        """
        # 标准化输入
        city_full = (city_full or "").strip()
        city_label = (city_label or "").strip()
        raw = (city_raw or "").strip()

        # 从原始城市字段中提取基础名称和数字后缀，例如“北京2”“西安114514”
        m = re.match(r"^(.+?)(\d+)?$", raw) if raw else None
        raw_base = m.group(1) if m else raw
        suffix = m.group(2) if m and m.group(2) else ""

        # 优先使用配置中的简称，其次使用原始城市的基础名称
        base_label = city_label or raw_base

        # 直辖市 / 特别行政区：只保留一级城市名称，不展示省份
        municipalities = {"北京", "上海", "天津", "重庆", "香港", "澳门"}
        if base_label in municipalities or raw_base in municipalities:
            base = base_label or raw_base
            return f"{base}{suffix}"

        prov = ""
        city_name = ""

        # 1）优先使用 CITY_OPTIONS 中配置的完整城市名（可能包含省、市）
        if city_full:
            if " " in city_full:
                # 形如“广东省 广州市” / “陕西省 西安市”
                prov_part, city_part = city_full.split(" ", 1)
                prov = prov_part.replace("省", "").replace("市", "").strip()
                # 城市名中如果带有数字后缀（例如从“郑州2”传入），需要先去掉尾部数字，避免后面重复追加
                cleaned_city = city_part.replace("省", "").replace("市", "").strip()
                city_name = re.sub(r"\d+$", "", cleaned_city)
            else:
                cleaned = city_full.replace("省", "").replace("市", "").strip()
                # 例如 city_full = "郑州2"（来自原始字段），此处要去掉尾部数字，只保留城市名“郑州”
                city_name = re.sub(r"\d+$", "", cleaned)

        # 2）如果配置里没有省份信息，尝试从 CITY_PROVINCE_MAP 中根据简称反查省份
        if not prov and base_label in CartonMarkGenerator.CITY_PROVINCE_MAP:
            prov = CartonMarkGenerator.CITY_PROVINCE_MAP[base_label]

        # 3）组装基础显示文案
        if prov and city_name:
            base = f"{prov} {city_name}".strip()
        else:
            base = city_name or base_label or raw_base

        # 4）追加数字后缀（如有）
        return f"{base}{suffix}"

    def load_template(self) -> bool:
        """加载模板文件"""
        if not os.path.exists(self.template_path):
            print(f"错误: 找不到模板文件 {self.template_path}")
            return False
        
        try:
            with open(self.template_path, 'rb') as f:
                self.content = bytearray(f.read())
            print(f"成功加载模板: {self.template_path}")
            return True
        except Exception as e:
            print(f"加载模板失败: {e}")
            return False
    
    def generate(self, po_num: str, warehouse: str, city_code: str, vendor_name: str, 
                 output_dir: str = None) -> bool:
        """
        生成箱唛文件
        
        Args:
            po_num: 采购单号（10位）
            warehouse: 目的仓
            city_code: 城市代码（1-8）
            vendor_name: 商家名称
            output_dir: 输出目录
            
        Returns:
            是否生成成功
        """
        if not self.load_template():
            return False
        
        # 验证城市代码
        if city_code not in self.CITY_OPTIONS:
            print(f"错误: 无效的城市代码 {city_code}")
            return False
        
        city_info = self.CITY_OPTIONS[city_code]
        city_label = city_info["label"]
        # 新规则：目的城市展示，例如：
        # - 北京      -> 北京
        # - 北京2     -> 北京2
        # - 广州      -> 广东 广州
        # 这里 generate 不带原始城市后缀，因此只会应用“省/市”精简规则
        selected_city = self._format_destination_city(city_info["city"], city_label)
        
        # 确定输出目录
        if output_dir is None:
            output_dir = os.path.expanduser("~/Desktop")
        
        # 生成输出文件名
        output_filename = f"{city_code}.{city_label}箱唛.pld"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n正在生成箱唛...")
        print(f"采购单号: {po_num}")
        print(f"目的仓: {warehouse}")
        print(f"目的城市: {selected_city}")
        print(f"商家名称: {vendor_name}")
        
        # 字段配置
        FIELD_CONFIG = [
            {"name": "采购单号", "old": "0000000000", "val": po_num, "len": 10},
            {"name": "目的城市", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": selected_city, "len": 32},
            {"name": "目的仓", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": warehouse, "len": 34},
            {"name": "商家名称", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": vendor_name, "len": 30}
        ]
        
        try:
            # 按长度从长到短排序处理，防止短占位符被长占位符干扰
            sorted_config = sorted(FIELD_CONFIG, key=lambda x: x["len"], reverse=True)
            
            for item in sorted_config:
                target_bytes = item["old"].encode('gbk')
                pos = self.content.find(target_bytes)
                
                # 如果找不到，尝试模糊匹配
                if pos == -1:
                    pos = self.content.find(target_bytes[:4])
                
                if pos != -1:
                    # 准备缓冲区
                    new_val_bytes = item["val"].encode('gbk', errors='ignore')
                    buffer = bytearray([0] * item["len"])
                    for i in range(min(len(new_val_bytes), item["len"])):
                        buffer[i] = new_val_bytes[i]
                    
                    # 覆盖
                    self.content[pos:pos + item["len"]] = buffer
                    print(f"[√] {item['name']} 替换成功")
                else:
                    print(f"[×] 警告: 未找到 {item['name']} 的位置")
            
            # 保存文件
            with open(output_path, 'wb') as f:
                f.write(self.content)
            
            print(f"\n成功生成: {output_path}")
            return True
        
        except Exception as e:
            print(f"生成失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_to_path(self, po_num: str, warehouse: str, city_code: str, vendor_name: str,
                         output_path: str, city_raw: str = None) -> bool:
        """
        生成箱唛文件到指定路径
        
        Args:
            po_num: 采购单号（10位）
            warehouse: 目的仓
            city_code: 城市代码（1-8）
            vendor_name: 商家名称
            output_path: 输出文件完整路径
            
        Returns:
            是否生成成功
        """
        if not self.load_template():
            return False
        
        # 支持两种情况：
        # 1）city_code 在预设 CITY_OPTIONS 中（老城市）；
        # 2）city_code 为新城市使用的通用编码（例如 99），此时完全依赖 city_raw 生成目的城市文案。
        city_info = self.CITY_OPTIONS.get(city_code)
        if city_info:
            selected_city = self._format_destination_city(city_info["city"], city_info["label"], city_raw)
        else:
            # 未预设城市：直接从原始城市字段推导，例如“郑州” -> “河南 郑州”
            selected_city = self._format_destination_city(city_full=city_raw or "", city_label="", city_raw=city_raw)
        
        print(f"\n正在生成箱唛...")
        print(f"采购单号: {po_num}")
        print(f"目的仓: {warehouse}")
        print(f"目的城市: {selected_city}")
        print(f"商家名称: {vendor_name}")
        
        # 字段配置
        FIELD_CONFIG = [
            {"name": "采购单号", "old": "0000000000", "val": po_num, "len": 10},
            {"name": "目的城市", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": selected_city, "len": 32},
            {"name": "目的仓", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": warehouse, "len": 34},
            {"name": "商家名称", "old": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ", "val": vendor_name, "len": 30}
        ]
        
        try:
            # 按长度从长到短排序处理，防止短占位符被长占位符干扰
            sorted_config = sorted(FIELD_CONFIG, key=lambda x: x["len"], reverse=True)
            
            for item in sorted_config:
                target_bytes = item["old"].encode('gbk')
                pos = self.content.find(target_bytes)
                
                # 如果找不到，尝试模糊匹配
                if pos == -1:
                    pos = self.content.find(target_bytes[:4])
                
                if pos != -1:
                    # 准备缓冲区
                    new_val_bytes = item["val"].encode('gbk', errors='ignore')
                    buffer = bytearray([0] * item["len"])
                    for i in range(min(len(new_val_bytes), item["len"])):
                        buffer[i] = new_val_bytes[i]
                    
                    # 覆盖
                    self.content[pos:pos + item["len"]] = buffer
                    print(f"[√] {item['name']} 替换成功")
                else:
                    print(f"[×] 警告: 未找到 {item['name']} 的位置")
            
            # 保存文件
            with open(output_path, 'wb') as f:
                f.write(self.content)
            
            print(f"\n成功生成: {output_path}")
            return True
        
        except Exception as e:
            print(f"生成失败: {e}")
            import traceback
            traceback.print_exc()
            return False
        

class ShantouBCartonMarkGenerator:
    """
    汕头B仓专用箱唛生成器。
    
    使用独立模板（放在项目根目录 templates/shantou_b_carton_mark.pld），
    根据 Excel 工作表中的字段：
    - 供应商
    - 入库库房
    - 需求单号
    - 产品规格
    动态定位并替换模板中的全角“Ｘ”占位符（不同字段长度可不相同）。
    """

    def __init__(self, template_path: str | None = None) -> None:
        if template_path is None:
            base_dir = _get_app_base_dir()
            template_path = base_dir / "templates" / "shantou_b_carton_mark.pld"

        self.template_path = str(template_path)
        self.content: bytearray | None = None

    def load_template(self) -> bool:
        """加载汕头B仓箱唛模板"""
        if not os.path.exists(self.template_path):
            print(f"[DEBUG] 汕头B仓箱唛模板不存在: {self.template_path}")
            return False

        try:
            with open(self.template_path, "rb") as f:
                self.content = bytearray(f.read())
            print(f"[DEBUG] 成功加载汕头B仓箱唛模板: {self.template_path}")
            return True
        except Exception as e:
            print(f"[DEBUG] 加载汕头B仓箱唛模板失败: {e}")
            return False

    def _replace_field_by_label(self, label: str, value: str) -> None:
        """
        根据中文标签（如“供应商”）在模板中查找对应的全角“Ｘ”占位符，并用 value 替换。

        占位长度自动从模板中解析：先找到标签，再向后扫描连续的“Ｘ”字符，
        这样不同字段的“Ｘ”长度可以不同，无需在代码里写死。
        """
        if self.content is None:
            return

        if value is None:
            value = ""

        try:
            label_bytes = label.encode("gbk")
            x_bytes = "Ｘ".encode("gbk")  # 全角 X，占位符
        except Exception as e:
            print(f"[DEBUG] 编码标签或占位符失败 ({label}): {e}")
            return

        pos_label = self.content.find(label_bytes)
        if pos_label == -1:
            print(f"[DEBUG] 汕头B仓箱唛: 未找到标签 '{label}'")
            return

        # 从标签之后开始查找第一个占位符“Ｘ”
        search_start = pos_label + len(label_bytes)
        pos_x = self.content.find(x_bytes, search_start)
        if pos_x == -1:
            print(f"[DEBUG] 汕头B仓箱唛: 未找到标签 '{label}' 后面的占位符")
            return

        # 统计连续“Ｘ”的字节长度
        end = pos_x
        max_len = len(self.content)
        step = len(x_bytes)
        while end + step <= max_len and self.content[end : end + step] == x_bytes:
            end += step

        field_byte_len = end - pos_x
        if field_byte_len <= 0:
            return

        # 按字段字节长度构造缓冲区，并按 GBK 写入新值（超长会被截断）
        try:
            new_val_bytes = value.encode("gbk", errors="ignore")
        except Exception as e:
            print(f"[DEBUG] 汕头B仓箱唛: 字段 '{label}' 编码失败: {e}")
            return

        buffer = bytearray(b"\x00" * field_byte_len)
        for i in range(min(len(new_val_bytes), field_byte_len)):
            buffer[i] = new_val_bytes[i]

        self.content[pos_x:end] = buffer
        print(f"[DEBUG] 汕头B仓箱唛: 字段 '{label}' 替换成功")

    def generate(
        self,
        seq_num: int,
        city: str,
        supplier: str,
        inbound_warehouse: str,
        demand_no: str,
        product_spec: str,
        output_dir: str | None = None,
    ) -> bool:
        """
        生成汕头B仓箱唛文件。

        Args:
            seq_num: 序号（来自工作表 A 列）
            city: 城市名称（例如“汕头”）
            supplier: 供应商名称
            inbound_warehouse: 入库库房（全称）
            demand_no: 需求单号
            product_spec: 产品规格
            output_dir: 输出目录
        """
        if not self.load_template():
            return False

        # 默认导出到桌面
        if not output_dir:
            output_dir = os.path.expanduser("~/Desktop")

        # 文件名规则：序号.汕头B仓箱唛.pld
        output_filename = f"{seq_num}.汕头B仓箱唛.pld"
        output_path = os.path.join(output_dir, output_filename)

        # 替换字段
        self._replace_field_by_label("供应商", supplier)
        self._replace_field_by_label("入库库房", inbound_warehouse)
        self._replace_field_by_label("需求单号", demand_no)
        self._replace_field_by_label("产品规格", product_spec)

        try:
            with open(output_path, "wb") as f:
                f.write(self.content or b"")
            print(f"[DEBUG] 成功生成汕头B仓箱唛: {output_path}")
            return True
        except Exception as e:
            print(f"[DEBUG] 保存汕头B仓箱唛失败: {e}")
            return False
