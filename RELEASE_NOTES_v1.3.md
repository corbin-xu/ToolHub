# ToolHub v1.3 发布说明

## 下载

- **Windows**: [ToolHub-1.3.exe](https://github.com/corbin-xu/ToolHub/releases/download/v1.3/ToolHub-1.3.exe)
- **macOS**: [ToolHub-1.3.dmg](https://github.com/corbin-xu/ToolHub/releases/download/v1.3/ToolHub-1.3.dmg)

---

## 新功能

### 汕头B仓箱唛模板更新

- 采用新模板「汕头B仓箱唛 - 副本」，替换原 `shantou_b_carton_mark.pld`
- **EPL采购单号**：新增字段，格式为 `EPL` + 13 位数字（如 `EPL0000000000000`）
- **需求单号**：格式调整为 `PR` + 7 位数字（如 `PR0000000`）
- **空值处理**：需求单号或 EPL 采购单号为空时，整段替换为空格，实现完全空显示

### Excel 结构变更（汕头B仓箱唛工作表）

| C 列行 | 字段 |
|--------|------|
| row+1 | 供应商 |
| row+2 | 入库库房 |
| row+3 | **EPL采购单号**（新增） |
| row+4 | 需求单号 |
| row+5 | 产品规格 |

---

## 格式校验

- **需求单号**：非空时须为 `PR` + 7 位数字，否则弹窗提示并跳过该行
- **EPL采购单号**：非空时须为 `EPL` + 13 位数字，否则弹窗提示并跳过该行
- **空值**：允许替换，会弹窗提示后继续

---

## 其他

- 版本号更新至 1.3
- GitHub Actions 支持 Mac DMG 自动构建
- 新增 `workflow_dispatch`，可手动触发 Mac 构建

---

## 系统要求

- **Windows**: Windows 7 或更高版本
- **macOS**: 支持 Apple Silicon 及 Intel 芯片
