"""
PLD文件解析器
用于解析和修改PLD格式的标签文件

PLD格式使用长度前缀的二进制结构：
- 每个字段前面有一个字节表示长度
- 格式: [长度字节][数据]
"""

import os
import re
import struct
from typing import Dict, Optional, Tuple


class PLDParser:
    """PLD文件解析器"""
    
    def __init__(self, pld_path: str):
        """
        初始化PLD解析器
        
        Args:
            pld_path: PLD文件路径
        """
        self.pld_path = pld_path
        self.content = None
        self.load()
    
    def load(self):
        """加载PLD文件"""
        try:
            with open(self.pld_path, 'rb') as f:
                self.content = f.read()
        except Exception as e:
            print(f"加载PLD文件失败: {e}")
    
    def extract_text_data(self) -> Dict[str, str]:
        """
        提取PLD文件中的文本数据（完整格式）
        
        Returns:
            包含标签数据的字典
        """
        if not self.content:
            return {}
        
        data = {}
        
        try:
            # 尝试解码文件内容，忽略非UTF-8字符
            content_str = self.content.decode('utf-8', errors='ignore')
            
            # 提取品牌 - 查找"品牌:"后面的文本
            brand_match = re.search(r'品牌:\s*([^\x00\n]+)', content_str)
            if brand_match:
                brand = brand_match.group(1).strip()
                # 清理非ASCII字符
                brand = ''.join(c for c in brand if ord(c) < 128 or ord(c) > 127)
                if brand:
                    data['brand'] = brand
            
            # 提取产品名称 - 查找JD-开头的产品
            product_match = re.search(r'(JD-[^\x00\n]+)', content_str)
            if product_match:
                product = product_match.group(1).strip()
                # 只保留到第一个非法字符
                product = product.split('\x00')[0].strip()
                if product:
                    data['product_name'] = product
            
            # 提取SKU - 查找10开头的12位数字（完整格式）
            sku_match = re.search(r'(100\d{9})', content_str)
            if sku_match:
                data['sku'] = sku_match.group(1)
            else:
                # 如果没找到完整格式，查找任何4位数字（短格式）
                sku_match = re.search(r'SKU:\s*(\d{4})', content_str)
                if sku_match:
                    data['sku'] = sku_match.group(1)
            
            # 提取69码 - 查找69开头的13位数字（完整格式）
            code69_match = re.search(r'(697\d{10})', content_str)
            if code69_match:
                data['code_69'] = code69_match.group(1)
            else:
                # 如果没找到完整格式，查找任何4位数字（短格式）
                code69_match = re.search(r'69码:\s*(\d{4})', content_str)
                if code69_match:
                    data['code_69'] = code69_match.group(1)
            
            # 提取SN序列号 - 查找SN或NB开头的完整序列
            sn_match = re.search(r'(SN\d+|NB\d+)', content_str)
            if sn_match:
                data['sn'] = sn_match.group(1)
            else:
                # 如果没找到完整格式，查找任何4位数字（日期部分）
                sn_match = re.search(r'SN序列号:\s*(\d{4})', content_str)
                if sn_match:
                    data['sn'] = sn_match.group(1)
            
            # 提取日期 - 查找日期后面的4位数字
            date_match = re.search(r'日期:\s*(\d{4})', content_str)
            if date_match:
                data['date'] = date_match.group(1)
        
        except Exception as e:
            print(f"提取文本数据失败: {e}")
        
        print(f"提取的数据: {data}")
        return data
    
    def _find_length_prefixed_field(self, content: bytes, search_text: bytes) -> Optional[Tuple[int, int]]:
        """
        查找长度前缀的字段
        
        Args:
            content: 文件内容
            search_text: 要查找的文本
            
        Returns:
            (长度字节位置, 数据开始位置) 或 None
        """
        pos = content.find(search_text)
        if pos == -1:
            return None
        
        # 查找前面的长度字节
        # 长度字节应该在数据前面，通常是1字节
        if pos > 0:
            length_byte = content[pos - 1]
            # 检查长度字节是否匹配数据长度
            if length_byte == len(search_text):
                return (pos - 1, pos)
        
        return None
    
    def _replace_length_prefixed_field(self, content: bytearray, old_text: bytes, new_text: bytes) -> int:
        """
        替换长度前缀的字段
        
        Args:
            content: 文件内容
            old_text: 旧文本
            new_text: 新文本
            
        Returns:
            替换次数
        """
        replaced_count = 0
        pos = 0
        
        while True:
            pos = content.find(old_text, pos)
            if pos == -1:
                break
            
            old_len = len(old_text)
            new_len = len(new_text)
            
            print(f"找到匹配: {old_text} 在位置 {pos}")
            
            # 检查前面是否有长度字节
            if pos > 0:
                length_byte = content[pos - 1]
                print(f"前面的字节: {length_byte}, 期望长度: {old_len}")
                
                if length_byte == old_len:
                    # 更新长度字节
                    content[pos - 1] = new_len
                    
                    # 替换文本
                    del content[pos:pos + old_len]
                    content[pos:pos] = new_text
                    replaced_count += 1
                    print(f"替换成功: {old_text} -> {new_text}")
                    
                    pos += new_len
                else:
                    # 即使长度字节不匹配，也尝试直接替换
                    print(f"长度字节不匹配，尝试直接替换")
                    del content[pos:pos + old_len]
                    content[pos:pos] = new_text
                    replaced_count += 1
                    pos += new_len
            else:
                # 如果在开头，直接替换
                del content[pos:pos + old_len]
                content[pos:pos] = new_text
                replaced_count += 1
                pos += new_len
        
        return replaced_count
    
    def replace_text_data(self, old_data: Dict[str, str], new_data: Dict[str, str]) -> bool:
        """
        替换PLD文件中的文本数据
        
        Args:
            old_data: 旧数据（从模板中提取）
            new_data: 新数据（用户输入）
            
        Returns:
            是否替换成功
        """
        if not self.content:
            print("错误: 文件内容为空")
            return False
        
        try:
            content = bytearray(self.content)
            replaced_count = 0
            
            print(f"开始替换数据...")
            print(f"旧数据: {old_data}")
            print(f"新数据: {new_data}")
            
            # 使用从模板中提取的旧数据进行替换
            
            # 替换品牌
            if 'brand' in new_data and new_data['brand']:
                if 'brand' in old_data and old_data['brand']:
                    old_brand = old_data['brand'].encode('utf-8')
                    new_brand = new_data['brand'].encode('utf-8')
                    print(f"替换品牌: {old_data['brand']} -> {new_data['brand']}")
                    count = self._replace_length_prefixed_field(content, old_brand, new_brand)
                    replaced_count += count
                    print(f"品牌替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有品牌信息，跳过品牌替换")
            
            # 替换产品名称
            if 'product_name' in new_data and new_data['product_name']:
                if 'product_name' in old_data and old_data['product_name']:
                    old_product = old_data['product_name'].encode('utf-8')
                    new_product = new_data['product_name'].encode('utf-8')
                    print(f"替换产品名称: {old_data['product_name']} -> {new_data['product_name']}")
                    count = self._replace_length_prefixed_field(content, old_product, new_product)
                    replaced_count += count
                    print(f"产品名称替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有产品名称信息，跳过产品名称替换")
            
            # 替换 SKU - 使用短格式
            if 'sku' in new_data and new_data['sku']:
                if 'sku' in old_data and old_data['sku']:
                    old_sku = old_data['sku']
                    # 转换为短格式（最后 4 位）
                    if len(old_sku) > 4:
                        old_sku = old_sku[-4:]
                    old_sku_bytes = old_sku.encode('utf-8')
                    new_sku_bytes = new_data['sku'].encode('utf-8')
                    print(f"替换 SKU: {old_sku} -> {new_data['sku']}")
                    count = self._replace_length_prefixed_field(content, old_sku_bytes, new_sku_bytes)
                    replaced_count += count
                    print(f"SKU 替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有 SKU 信息，跳过 SKU 替换")
            
            # 替换 69码 - 使用短格式
            if 'code_69' in new_data and new_data['code_69']:
                if 'code_69' in old_data and old_data['code_69']:
                    old_code = old_data['code_69']
                    # 转换为短格式（最后 4 位）
                    if len(old_code) > 4:
                        old_code = old_code[-4:]
                    old_code_bytes = old_code.encode('utf-8')
                    new_code_bytes = new_data['code_69'].encode('utf-8')
                    print(f"替换 69码: {old_code} -> {new_data['code_69']}")
                    count = self._replace_length_prefixed_field(content, old_code_bytes, new_code_bytes)
                    replaced_count += count
                    print(f"69码替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有 69码 信息，跳过 69码 替换")
            
            # 替换 SN - 使用日期部分
            if 'sn' in new_data and new_data['sn']:
                if 'sn' in old_data and old_data['sn']:
                    old_sn = old_data['sn']
                    # 提取日期部分（倒数第7到倒数第4位）
                    if len(old_sn) > 4:
                        numbers = re.sub(r'[^0-9]', '', old_sn)
                        if len(numbers) >= 7:
                            old_sn = numbers[-7:-3]
                    old_sn_bytes = old_sn.encode('utf-8')
                    new_sn_bytes = new_data['sn'].encode('utf-8')
                    print(f"替换 SN 日期: {old_sn} -> {new_data['sn']}")
                    count = self._replace_length_prefixed_field(content, old_sn_bytes, new_sn_bytes)
                    replaced_count += count
                    print(f"SN 日期替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有 SN 信息，跳过 SN 替换")
            
            # 替换日期
            if 'date' in new_data and new_data['date']:
                if 'date' in old_data and old_data['date']:
                    old_date = old_data['date'].encode('utf-8')
                    new_date = new_data['date'].encode('utf-8')
                    print(f"替换日期: {old_data['date']} -> {new_data['date']}")
                    count = self._replace_length_prefixed_field(content, old_date, new_date)
                    replaced_count += count
                    print(f"日期替换 {count} 次")
                else:
                    print(f"警告: 旧数据中没有日期信息，跳过日期替换")
            
            print(f"总共替换了 {replaced_count} 个字段")
            
            if replaced_count > 0:
                self.content = bytes(content)
                return True
            else:
                print("警告: 没有替换任何字段，但继续保存文件")
                # 即使没有替换任何字段，也返回 True（因为文件本身是有效的）
                return True
        
        except Exception as e:
            print(f"替换文本数据失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save(self, output_path: str) -> bool:
        """
        保存PLD文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            是否保存成功
        """
        if not self.content:
            return False
        
        try:
            with open(output_path, 'wb') as f:
                f.write(self.content)
            return True
        except Exception as e:
            print(f"保存PLD文件失败: {e}")
            return False
