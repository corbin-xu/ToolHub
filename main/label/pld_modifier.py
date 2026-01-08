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
    
    def replace_field(self, placeholder: str, new_value: str, field_length: int, encoding: str = 'gbk', max_replacements: int = None) -> bool:
        """
        替换字段
        
        Args:
            placeholder: 占位符（如 "SG0000000000"、"品牌：ＸＸＸＸ"）
            new_value: 新值
            field_length: 字段长度
            encoding: 编码方式（默认 gbk）
            max_replacements: 最大替换次数（None 表示替换所有）
            
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
            
            # 替换指定次数的出现位置
            replaced_count = 0
            while pos != -1 and (max_replacements is None or replaced_count < max_replacements):
                self.content[pos:pos + field_length] = buffer
                pos = self.content.find(target, pos + 1)
                replaced_count += 1
            
            print(f"[√] '{placeholder}' -> '{new_value}' (替换 {replaced_count} 次)")
            return True
        
        except Exception as e:
            print(f"[×] 替换失败: {e}")
            return False
    
    def replace_date_placeholder(self, new_date: str, encoding: str = 'gbk') -> bool:
        """
        自动检测并替换右上角的日期占位符（仅替换一次）
        
        Args:
            new_date: 新日期（MMDD 格式，如 "1229"）
            encoding: 编码方式（默认 gbk）
            
        Returns:
            是否替换成功
        """
        if not self.content or len(new_date) != 4:
            return False
        
        try:
            import re
            
            # 将内容转换为字符串以便搜索
            content_str = self.content.decode(encoding, errors='ignore')
            
            # 查找所有可能的日期占位符（MMDD 格式）
            # 匹配 01-12 月份和 01-31 天数
            date_pattern = r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])'
            
            matches = list(re.finditer(date_pattern, content_str))
            
            if not matches:
                print("警告: 找不到日期占位符")
                return False
            
            # 只替换第一个找到的日期占位符（右上角通常是第一个）
            match = matches[0]
            old_date = match.group(0)
            
            if old_date != new_date:
                return self.replace_field(old_date, new_date, 4, encoding=encoding, max_replacements=1)
            
            return False
        
        except Exception as e:
            print(f"[×] 自动替换日期失败: {e}")
            return False
    
    def replace_datetime_placeholder(self, new_datetime: str, encoding: str = 'gbk') -> bool:
        """
        自动检测并替换年份+日期占位符（仅在 SN 序列号中）
        
        Args:
            new_datetime: 新日期时间（YYMMDD 或 YYYYMMDD 格式）
            encoding: 编码方式（默认 gbk）
            
        Returns:
            是否替换成功
        """
        if not self.content:
            return False
        
        try:
            import re
            
            # 将内容转换为字符串以便搜索
            content_str = self.content.decode(encoding, errors='ignore')
            
            replaced_count = 0
            
            if len(new_datetime) == 6:
                # YYMMDD 格式（3C标签 - SG/SN）
                # SN 格式: SG/SN + 序号(1-3位) + 年份(2位) + 日期(4位) + 批次(3位)
                # 例如: SG119260122900001 -> SG119261229001
                # 年份在倒数第 9-7 位，日期在倒数第 7-3 位
                
                # 查找所有 SG/SN 开头的 SN 序列号
                sn_pattern = r'(SG|SN)(\d+?)(\d{2})(\d{4})(\d{3})'
                
                matches = list(re.finditer(sn_pattern, content_str))
                
                for match in matches:
                    old_datetime = match.group(3) + match.group(4)  # 年份(2) + 日期(4)
                    if old_datetime != new_datetime:
                        # 构建完整的旧 SN
                        old_sn = match.group(0)
                        # 构建新 SN
                        new_sn = match.group(1) + match.group(2) + new_datetime + match.group(5)
                        
                        if self.replace_field(old_sn, new_sn, len(old_sn), encoding=encoding):
                            replaced_count += 1
            
            elif len(new_datetime) == 8:
                # YYYYMMDD 格式（玩具标签 - NB）
                # SN 格式: NB + 序号(1-3位) + 年份(4位) + 日期(4位) + 批次(3位)
                # 例如: NB119202612291001 -> NB119202712291001
                # 年份在倒数第 11-7 位，日期在倒数第 7-3 位
                
                # 查找所有 NB 开头的 SN 序列号
                sn_pattern = r'(NB)(\d+?)(\d{4})(\d{4})(\d{3})'
                
                matches = list(re.finditer(sn_pattern, content_str))
                
                for match in matches:
                    old_datetime = match.group(3) + match.group(4)  # 年份(4) + 日期(4)
                    if old_datetime != new_datetime:
                        # 构建完整的旧 SN
                        old_sn = match.group(0)
                        # 构建新 SN
                        new_sn = match.group(1) + match.group(2) + new_datetime + match.group(5)
                        
                        if self.replace_field(old_sn, new_sn, len(old_sn), encoding=encoding):
                            replaced_count += 1
            
            return replaced_count > 0
        
        except Exception as e:
            print(f"[×] 自动替换日期时间失败: {e}")
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
