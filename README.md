# JD Supplier Label Generator

电商工具箱 - 一个功能强大的电商数据处理工具

## 功能特性

- **标签生成** - 支持 3C、玩具等多种产品标签生成
- **箱唛生成** - 自动生成箱唛标签
- **预定表导出** - 生成预定表 Excel 文件
- **关键词分析** - 分析关键词数据和优化建议
- **批量处理** - 支持批量导入和导出

## 系统要求

- Windows 7 或更高版本
- Python 3.8+ (如果从源代码运行)

## 安装

### 方式一：使用安装程序（推荐）

下载最新的 `jd-supplier-label-generator-1.0.0-setup.exe` 并运行安装程序。

### 方式二：从源代码运行

1. 克隆仓库：
```bash
git clone https://github.com/corbin-xu/JD Supplier Label Generator.git
cd JD Supplier Label Generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python gui_app.py
```

## 使用方法

### 标签生成
1. 点击"标签箱唛"标签页
2. 点击"导入"按钮选择 Excel 文件
3. 选择工作表和产品类型
4. 点击"导出"生成标签

### 预定表导出
1. 在"输出内容"中勾选"预定表"
2. 设置预计到货日期
3. 点击"导出"生成预定表

### 关键词分析
1. 点击"关键词分析"标签页
2. 导入 CSV 数据文件
3. 查看分析结果和优化建议

## 设置

点击左下角"设置"按钮可以：
- 查看当前版本信息
- 检测更新
- 设置导出路径

## 开发者

- **GitHub**: [corbin-xu](https://github.com/corbin-xu)
- **邮箱**: corbinxu@outlook.com

## 许可证

MIT License - 详见 LICENSE 文件

## 更新日志

### v1.0.0 (2026-01-06)
- 初始版本发布
- 支持标签和箱唛生成
- 支持预定表导出
- 支持关键词分析
