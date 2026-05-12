# GRIT v3.3 — Circle Internet (CRCL) 实战版

**发布日期**：2026-05-13

---

## 概述

v3.3 是 GRIT 框架首次应用于**纯美国本土上市公司**（之前 FUFU 是海外公司美股上市）的里程碑版本。以 Circle Internet (CRCL) 为标的完成完整分析，驱动了框架的三大能力升级。

---

## 新增能力

### 1. SEC XBRL 自动转换 ✅ 验证

**问题**：SEC 10-K/10-Q/424B4 以 iXBRL 格式发布（HTML 嵌入 XBRL 标签），Agent 直接 grep 无法阅读。

**方案**：开发 `tools/sec_xbrl_to_text.py`，剥离 `<ix:>` 标签 + `<ix:hidden>` 块 + `display:none` div，输出纯文本。

```bash
find raw/ -name "*.html" -print0 | while IFS= read -r -d '' f; do
  python3 tools/sec_xbrl_to_text.py "$f" "${f%.html}_parsed.txt"
done
```

**验证**：CRCL 2026Q1 10-Q PDF vs XBRL parsed 对照 — **95.8% 字符覆盖率，零实质性文字遗漏**。差异仅来自 SEC 封面样板（表单复选框/CIK编号等 XBRL 元数据）。

**集成**：GRIT SKILL.md HARNESS 步骤1 增加自动转换检查项。

### 2. 非上市竞对数据提取

**问题**：Tether 未上市，无完整财报，仅发布 BDO 鉴证报告（Attestation Report）。

**方案**：`references/tether-competitor-extraction.md` — BDO 报告正则提取模板：

| 提取项 | 正则模式 |
|:---|:---|
| 总资产 | `amount to US\$ ([\d,]+)` |
| USDT 流通量 | `liabilities.*?amount to US\$ ([\d,]+)` |
| 季度利润 | `liabilities.*?by US\$ ([\d,]+)` |
| 国债占比 | `U.S. Treasury Bills.*?([\d,]+)` |
| BTC 持仓 | `Bitcoin.*?([\d,]+)` |

**结果**：Tether Q1'26 季度利润 $82.3 亿 vs Circle $0.55 亿 — 50 倍差距。竞对数据置信度标注为「中」（非完整审计财报）。

### 3. 三维估值框架

**问题**：Circle 同时拥有「利差型金融业务」+「支付网络业务」+「区块链基础设施业务」，单一 PE 框架会误判。

**方案**：`references/special-business-models.md` 增加稳定币估值指引：

| 维度 | 业务 | 估值逻辑 | 锚点 |
|:---|:---|:---|:---|
| 第一维 | 储备利息收入 | 银行/利差型 | 8-15x PE（地板） |
| 第二维 | CPN + Other 收入 | Visa/支付网络型 | 24-30x PE（转折） |
| 第三维 | Arc L1 + ARC Token | 基础设施/生态期权 | 期权定价（未来） |

### 4. 实时数据源验证

Yahoo Finance v8 chart 端点：已验证 CRCL/AAPL/TSLA/PYPL 均可正常返回。quoteSummary 端点仍被封。PE/市值自算流程已更新到 `references/real-time-data-sources.md`。

---

## 文件变更

```
新增:
  references/GRIT模板-v1.40.md           ← 三级信息整合 + IC卡 + 信息→假设传导表
  references/market-hk.md                ← 港股市场参考（预留）
  references/yahoo-finance-pitfalls.md    ← Yahoo Finance API 实战陷阱
  references/non-recurring-adjustment.md  ← 非经常性损益剔除流程
  references/special-business-models.md   ← 特殊商业模式处理
  references/tether-competitor-extraction.md ← 非上市竞对提取
  tools/sec_xbrl_to_text.py               ← SEC iXBRL 转换器

更新:
  SKILL.md                               ← v3.3，集成 XBRL 自动转换
  references/real-time-data-sources.md   ← Yahoo v8 验证 + 多ticker测试
  README.md                              ← v3.3 能力说明
```

---

## 向后兼容

- 所有 v3.2 流程保持不变
- A股/港股分析路径无变更
- XBRL 转换仅在有 `.html` 文件时触发，无 HTML 则跳过
- 三维估值框架仅触发于特殊商业模式检测（稳定币/平台型等）

---

## 已知限制

- XBRL 转换：多列表格变线性文本，财务数据仍优先用 Excel
- Tether 数据：BDO 鉴证非完整审计，置信度最高「中」
- ARC Token $30 亿 FDV 基于预售价格，非公开市场定价
- Yahoo Finance chart 端点不返回 marketCap/PE，需自算

---

## CRCL 分析成果

报告：961 行 / 68,201 字符 / 15 处 SEC 一手引用 / 7 处独立研究引用

核心结论：部分符合「3年业绩1变2」，但当前 $328 亿市值高于买入阈值 $150 亿。最大的不确定性来自利率路径和 Coinbase 协议重谈。

[完整报告](https://github.com/panfeng0806/grit-stock-analysis)
