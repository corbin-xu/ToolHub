#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
箱唛生成工具 - 基于模板的箱唛文件生成
"""

import os
import shutil
from pathlib import Path


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
    
    def __init__(self, template_path: str = None):
        """初始化箱唛生成器"""
        if template_path is None:
            # 使用相对路径查找模板
            current_dir = Path(__file__).parent.parent.parent
            template_path = current_dir / "templates" / "carton_mark.pld"
        
        self.template_path = str(template_path)
        self.content = None
    
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
        selected_city = city_info["city"]
        city_label = city_info["label"]
        
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
                         output_path: str) -> bool:
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
        
        # 验证城市代码
        if city_code not in self.CITY_OPTIONS:
            print(f"错误: 无效的城市代码 {city_code}")
            return False
        
        city_info = self.CITY_OPTIONS[city_code]
        selected_city = city_info["city"]
        
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

