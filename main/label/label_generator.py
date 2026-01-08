"""
标签箱唛生成工具
支持生成PLD格式的标签文件
"""

import os
import re
import shutil
from datetime import datetime
from typing import Optional, Tuple
from main.label.pld_parser import PLDParser
from main.label.pld_modifier import PLDModifier


class LabelGenerator:
    """PLD标签生成器"""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        初始化标签生成器
        
        Args:
            template_path: PLD模板文件路径
        """
        self.label_data = {}
        self.template_path = template_path
    
    @staticmethod
    def build_sn(brand_prefix: str, seq_num: str, year: str, date: str, batch: str) -> str:
        """
        构建 SN 序列号
        
        格式: [品牌][序号][年份][日期][批次]
        例如: SN1260522001 = SN + 1 + 26 + 0522 + 001
        
        Args:
            brand_prefix: 品牌前缀（SN 或 NB）
            seq_num: 序号（1-3位数字）
            year: 年份（SN为2位，NB为4位）
            date: 日期（4位MMDD）
            batch: 批次（3位）
            
        Returns:
            完整的 SN 序列号
        """
        return f"{brand_prefix}{seq_num}{year}{date}{batch}"
    
    @staticmethod
    def parse_sn(sn: str) -> Tuple[str, str, str, str, str]:
        """
        解析 SN 序列号
        
        格式: [品牌][序号][年份][日期][批次]
        例如: SN1260522001 = SN + 1 + 26 + 0522 + 001
        
        Args:
            sn: SN 序列号
            
        Returns:
            (品牌, 序号, 年份, 日期, 批次)
        """
        # 提取品牌前缀（SN 或 NB 等）
        match = re.match(r'^([A-Z]+)(\d+)$', sn)
        if not match:
            return ('', '', '', '', '')
        
        brand_prefix = match.group(1)
        numbers = match.group(2)
        
        # 根据品牌前缀确定年份长度
        # SN: 年份是 2 位（如 26 表示 2026）
        # NB: 年份是 4 位（如 2025）
        # SG: 年份是 2 位（如 26 表示 2026）
        if brand_prefix == 'SN':
            year_len = 2
        elif brand_prefix == 'NB':
            year_len = 4
        elif brand_prefix == 'SG':
            year_len = 2
        else:
            year_len = 2
        
        # 解析结构：序号(1-3位) + 年份 + 日期(4位) + 批次(3位)
        # 从后往前提取：批次(3) + 日期(4) + 年份 + 序号
        batch = numbers[-3:] if len(numbers) >= 3 else ''
        date = numbers[-7:-3] if len(numbers) >= 7 else ''
        year = numbers[-(7+year_len):-7] if len(numbers) >= (7+year_len) else ''
        seq_num = numbers[:-(7+year_len)] if len(numbers) >= (7+year_len) else numbers
        
        return (brand_prefix, seq_num, year, date, batch)
    
    @staticmethod
    def extract_short_sku(sku: str) -> str:
        """
        从完整 SKU 中提取短格式（最后 4 位数字）
        
        Args:
            sku: 完整 SKU（如 100140692276）
            
        Returns:
            短格式 SKU（最后 4 位，如 2276）
        """
        # 提取所有数字
        numbers = re.sub(r'[^0-9]', '', sku)
        # 返回最后 4 位
        return numbers[-4:] if len(numbers) >= 4 else numbers
    
    @staticmethod
    def extract_short_code69(code69: str) -> str:
        """
        从完整 69码 中提取短格式（最后 4 位数字）
        
        Args:
            code69: 完整 69码（如 6978030410332）
            
        Returns:
            短格式 69码（最后 4 位，如 0332）
        """
        # 提取所有数字
        numbers = re.sub(r'[^0-9]', '', code69)
        # 返回最后 4 位
        return numbers[-4:] if len(numbers) >= 4 else numbers
    
    def set_label_data(self, brand: str, product_name: str, sku: str, 
                       code_69: str, sn: str, date: Optional[str] = None):
        """
        设置标签数据
        
        Args:
            brand: 品牌名称
            product_name: 产品名称
            sku: SKU码
            code_69: 69码
            sn: SN序列号
            date: 日期（格式：MMDD，如0605）
        """
        if not date:
            date = datetime.now().strftime("%m%d")
        
        self.label_data = {
            'brand': brand,
            'product_name': product_name,
            'sku': sku,
            'code_69': code_69,
            'sn': sn,
            'date': date
        }
    
    def set_template(self, template_path: str) -> bool:
        """
        设置PLD模板文件
        
        Args:
            template_path: 模板文件路径
            
        Returns:
            是否设置成功
        """
        if os.path.exists(template_path):
            self.template_path = template_path
            return True
        return False
    
    def generate_pld(self, output_dir: str = None, seq_num: str = None, use_seq_prefix: bool = True) -> bool:
        """
        生成PLD文件
        
        Args:
            output_dir: 输出目录（如果为 None，使用桌面）
            seq_num: 序号（如果为 None，从 SN 中解析）
            use_seq_prefix: 是否在文件名中添加序号前缀（默认 True）
            
        Returns:
            是否生成成功
        """
        if not self.label_data:
            print("错误: 标签数据为空")
            return False
        
        try:
            # 确定输出目录
            if output_dir is None:
                output_dir = os.path.expanduser("~/Desktop")
            
            # 获取序号和日期
            date = None
            if seq_num is None:
                # 从 SN 中提取序号
                sn = self.label_data.get('sn', '')
                brand_prefix, seq_num, year, date, batch = self.parse_sn(sn)
                print(f"解析 SN: {sn} -> 序号={seq_num}, 日期={date}")
            else:
                print(f"使用提供的序号: {seq_num}")
                # 从标签数据中获取日期
                date = self.label_data.get('date', '')
            
            # 获取完整 SN
            sn_full = self.label_data.get('sn', '')
            sn_len = len(sn_full)
            
            # 生成文件名
            product_name = self.label_data.get('product_name', 'label')
            if use_seq_prefix:
                filename = f"{seq_num}.{product_name}.pld"
            else:
                filename = f"{product_name}.pld"
            output_path = os.path.join(output_dir, filename)
            print(f"输出路径: {output_path}")
            
            # 根据 SN 长度查找模板文件
            template_path = os.path.join(os.path.dirname(self.template_path), f"label_{sn_len}.pld")
            
            if not os.path.exists(template_path):
                # 如果按长度命名的模板不存在，使用默认模板
                template_path = self.template_path
            
            if not os.path.exists(template_path):
                print(f"错误: 找不到模板文件 {template_path}")
                return False
            
            print(f"使用模板文件: {template_path}")
            
            try:
                # 复制模板文件到输出位置
                shutil.copy(template_path, output_path)
                print(f"模板文件已复制到: {output_path}")
                
                # 使用 PLDModifier 修改文件
                modifier = PLDModifier(output_path)
                
                # 定义字段配置
                fields = [
                    {
                        "name": "SN码",
                        "placeholder": "SG" + "0" * (sn_len - 2),  # 如 SG0000000000
                        "value": sn_full,
                        "length": sn_len
                    },
                    {
                        "name": "品牌",
                        "placeholder": "品牌：ＸＸＸＸ",
                        "value": f"品牌：{self.label_data.get('brand', '')}",
                        "length": 14
                    },
                    {
                        "name": "产品",
                        "placeholder": "ＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸＸ",
                        "value": product_name,
                        "length": 32
                    },
                    {
                        "name": "SKU",
                        "placeholder": "000000000000",
                        "value": self.label_data.get('sku', ''),
                        "length": 12
                    },
                    {
                        "name": "69码",
                        "placeholder": "6900000000000",
                        "value": self.label_data.get('code_69', ''),
                        "length": 13
                    },
                    {
                        "name": "日期",
                        "placeholder": "0000",
                        "value": date if date else self.label_data.get('date', ''),
                        "length": 4
                    }
                ]
                
                # 替换所有字段
                print("\n正在处理模板数据...")
                for field in fields:
                    if field["value"]:
                        modifier.replace_field(
                            field["placeholder"],
                            field["value"],
                            field["length"],
                            encoding='gbk'
                        )
                
                # 保存修改
                if modifier.save(output_path):
                    print(f"\n文件已保存: {output_path}")
                    return True
                else:
                    print(f"文件保存失败")
                    return False
            
            except Exception as e:
                print(f"修改模板文件失败: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        except Exception as e:
            print(f"生成PLD文件失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_text_label(self, output_path: str) -> bool:
        """
        生成文本格式的标签（用于预览）
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            是否生成成功
        """
        if not self.label_data:
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("【套装无拆】\n")
                f.write(f"品牌: {self.label_data['brand']}\n")
                f.write(f"名称: {self.label_data['product_name']}\n")
                f.write(f"SKU: {self.label_data['sku']}\n")
                f.write(f"69码: {self.label_data['code_69']}\n")
                f.write(f"SN序列号: {self.label_data['sn']}\n")
                f.write(f"日期: {self.label_data['date']}\n")
            
            return True
        except Exception as e:
            print(f"生成文本标签失败: {e}")
            return False
    
    def get_label_preview(self) -> str:
        """获取标签预览文本"""
        if not self.label_data:
            return "未设置标签数据"
        
        preview = f"""
【套装无拆】
品牌: {self.label_data['brand']}
名称: {self.label_data['product_name']}
SKU: {self.label_data['sku']}
69码: {self.label_data['code_69']}
SN序列号: {self.label_data['sn']}
日期: {self.label_data['date']}
        """.strip()
        
        return preview
