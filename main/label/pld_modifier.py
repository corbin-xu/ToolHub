#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD 文件修改器 - 基于占位符替换的正确方法
"""


class PLDModifier:
    """PLD 文件修改器"""
    
    def __init__(self, pld_path: str):
        """初始化修改器"""
        self.pld_path = pld_path
        self.content = None
        self.load()
    
    def load(self):
        """加载 PLD 文件"""
        try:
            with open(self.pld_path, 'rb') as f:
                self.content = bytearray(f.read())
            print(f"成功加载 PLD 文件: {self.pld_path}")
        except Exception as e:
            print(f"加载 PLD 文件失败: {e}")
    
    def replace_field(self, placeholder: str, new_value: str, field_length: int, encoding: str = 'gbk') -> bool:
        """
        替换字段
        
        Args:
            placeholder: 占位符（如 "SG0000000000"、"品牌：ＸＸＸＸ"）
            new_value: 新值
            field_length: 字段长度
            encoding: 编码方式（默认 gbk）
            
        Returns:
            是否替换成功
        """
        if not self.content:
            print("错误: 文件内容为空")
            return False
        
        try:
            # 编码占位符
            target = placeholder.encode(encoding)
            pos = self.content.find(target)
            
            if pos == -1:
                print(f"警告: 找不到占位符 '{placeholder}'")
                return False
            
            # 编码新值并用 Null 填充保持长度
            new_bytes = new_value.encode(encoding, errors='ignore')
            buffer = bytearray([0] * field_length)
            for i in range(min(len(new_bytes), field_length)):
                buffer[i] = new_bytes[i]
            
            # 替换所有出现的位置
            replaced_count = 0
            while pos != -1:
                self.content[pos:pos + field_length] = buffer
                pos = self.content.find(target, pos + 1)
                replaced_count += 1
            
            print(f"[√] '{placeholder}' -> '{new_value}' (替换 {replaced_count} 次)")
            return True
        
        except Exception as e:
            print(f"[×] 替换失败: {e}")
            return False
    
    def save(self, output_path: str) -> bool:
        """保存修改后的 PLD 文件"""
        if not self.content:
            print("错误: 文件内容为空")
            return False
        
        try:
            with open(output_path, 'wb') as f:
                f.write(self.content)
            print(f"成功保存 PLD 文件: {output_path}")
            return True
        except Exception as e:
            print(f"保存 PLD 文件失败: {e}")
            return False
