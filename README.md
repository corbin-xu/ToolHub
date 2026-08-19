# 京东供应商标签生成器

用于批量生成京东供应商标签、箱唛和预定表的桌面应用。

## 功能特性

- **标签生成** - 支持 3C、玩具等多种产品标签生成
- **箱唛生成** - 自动生成箱唛标签
- **预定表导出** - 生成预定表 Excel 文件
- **批量处理** - 支持批量导入和导出

## 系统要求

- Windows 7 或更高版本
- Python 3.8+ (如果从源代码运行)

## 安装

### 方式一：使用安装程序（推荐）

下载最新的 `jd-supplier-label-generator-1.1.0.exe` 并运行安装程序。

### 方式二：从源代码运行

1. 克隆仓库：
```bash
git clone https://github.com/xgb819/jd-supplier-label-generator.git
cd jd-supplier-label-generator
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
1. 点击"导入 Excel"选择数据文件
2. 选择工作表和产品类型
3. 选择需要生成的内容
4. 点击"导出文件"生成标签或箱唛

### 预定表导出
1. 在"输出内容"中勾选"预定表"
2. 设置预计到货日期
3. 点击"导出文件"生成预定表

## 设置

点击界面右上角的"应用设置"按钮可以：
- 查看当前版本信息
- 检测更新
- 设置导出路径

## 开发者

- **GitHub**: [xgb819](https://github.com/xgb819)
- **邮箱**: xgb819@gmail.com

提交代码时请使用 **英文** 编写 commit message，避免在 GitHub 上出现乱码。

## 许可证

MIT License - 详见 LICENSE 文件

### v1.0.0 (2026-01-06)
- 初始版本发布
- 支持标签和箱唛生成
- 支持预定表导出
