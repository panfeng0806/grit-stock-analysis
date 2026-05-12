# GRIT 五要素股票研究 v3.3

> AI Agent 通用投研技能包 — 让任何 AI Agent 都能产出研报级别的股票分析

---

## 概述

GRIT 是一个结构化的股票投研流程框架，将「原始资料 → 结构化素材 → 深度分析 → 完整报告」串成一条单向流水线。它不是财务数据查询工具——它是一套让 AI Agent 像分析师一样思考的认知流程。

**五要素**：需求、竞争、资本、估值、风险。

**v3.3 新增**：纯美股上市公司的完整分析能力（CRCL 实战验证），SEC XBRL 自动转换，Tether 等非上市竞对数据提取，三维估值框架（银行+Visa+期权）。

---

## 适用市场

| 市场 | 判定依据 | 数据源 |
|:---|:---|:---|
| A 股 | 代码纯数字 / 用户指定 | Wind/Choice Excel、东方财富 API、问财 API、巨潮资讯网 |
| 美股 | 代码含字母 / raw 中有 10-K/10-Q/424B4 | SEC EDGAR (XBRL 自动转换)、Yahoo Finance v8、CoinGecko |
| 港股 | 代码 5 位数字 / .HK 后缀 | 港交所披露易、Yahoo Finance v8、Wind Excel |

阶段 0 自动检测市场，加载对应参考文件。美股新增：XBRL 自动转换（验证覆盖率 95.8%）、非上市竞对数据正则提取（Tether BDO 鉴证报告）。

---

## 工作流程

```
阶段0: 项目初始化（市场检测 → 创建文件夹 → 输出资料清单）
阶段1: 扫描与覆盖评估（扫描 raw/ → 覆盖-缺口矩阵 → 用户决策）
══════════════════════════════════════════════ ← 用户交互线
🔄 HARNESS v2.0 执行引擎
   步骤1: 全量文件扫描（pdftotext 预检 + SEC XBRL 自动转换）
   步骤2: 按业务线逐线提取（B1-B7 七类信息）
   步骤3: 假设溯源表（来源链+推导+置信度）
   步骤4: 按 GRIT 模板 v1.40 输出报告
══════════════════════════════════════════════
输出前自检（HARNESS 六项 + 数据质量 + 深度 + 一致性）
```

---

## 文件结构

```
grit-stock-analysis/
├── SKILL.md                              ← 核心流程（自包含所有执行规则）
├── references/
│   ├── GRIT模板-v1.40.md                 ← 报告模板（三级信息整合 + IC卡）
│   ├── real-time-data-sources.md         ← 全市场实时数据源（A股/美股/加密）
│   ├── market-a-share.md                 ← A股：Wind Excel / 东方财富 / 问财
│   ├── market-us.md                      ← 美股：SEC章节导航 / 10-K提取 / Yahoo Finance
│   ├── market-hk.md                      ← 港股：港交所披露易 / Wind Excel
│   ├── formulas.md                       ← 衍生指标自动计算公式
│   ├── wind-excel-structure.md           ← Wind/Choice Excel 行区块结构
│   ├── yahoo-finance-pitfalls.md         ← Yahoo Finance API 踩坑记录
│   ├── non-recurring-adjustment.md       ← 非经常性损益剔除流程
│   ├── special-business-models.md        ← 特殊商业模式处理（稳定币/加密等）
│   └── tether-competitor-extraction.md   ← 非上市竞对BDO鉴证报告提取
└── tools/
    └── sec_xbrl_to_text.py               ← SEC iXBRL HTML → 纯文本转换器
```

---

## 安装

GRIT 不依赖任何特定 Agent——**它就是一堆 Markdown 文件**。放到你 AI Agent 加载 skills / context documents 的目录下即可。

| Agent | 放置位置 |
|:---|:---|
| Hermes | `~/.hermes/skills/research/grit-stock-analysis/` |
| OpenClaw | 项目根目录或自定义 skills 文件夹 |
| Claude Code | 项目 `.claude/commands/` 或通过 CLAUDE.md 引用 |
| Cursor | 项目根目录，通过 `.cursorrules` 引用 |
| 其他 | 任何 Agent 能读取到的路径即可 |

```bash
git clone https://github.com/panfeng0806/grit-stock-analysis.git /你的/skills/目录/grit-stock-analysis
```

> XBRL 转换工具依赖：Python 3 标准库（无需额外安装 pip 包）。

---

## 使用方式

1. 将标的原始资料（年报 PDF/HTML、财务 Excel、券商研报、调研纪要等）放入 `raw/` 文件夹
2. 对 Agent 说：「分析一下 XXX（代码 XXX）」
3. Agent 自动执行六阶段流程，产出完整报告

**输出**：

```
~/grit/analysis/{股票名称}（{股票代码}）/
├── raw/             ← 原始资料
└── report.md        ← 完整 GRIT 报告（模板 v1.40 格式，唯一输出文件）
```

---

## v3.3 核心能力

### 纯美股完整支持
- SEC 10-K/10-Q/424B4/S-1 iXBRL 自动转换（已验证 95.8% 覆盖率）
- Item 1-16 全章节遍历（业务/风险/MD&A/高管/股东/财报）
- 三类普通股投票权结构提取（Class A/B/C）
- Evergreen 股权池稀释风险识别

### 非传统竞对数据
- Tether BDO 鉴证报告正则提取（总资产/负债/超额利润/储备构成）
- 非上市竞对置信度自动降级标注

### 三维估值框架
- 第一维：利息业务 → 银行 PE（地板价）
- 第二维：CPN/支付 → Visa PE（转折价）
- 第三维：Arc/代币 → 生态期权（未来价）

### 实时数据源
- Yahoo Finance v8 chart 端点（已验证 CRCL/AAPL/TSLA/PYPL）
- 东方财富 API（A股）
- CoinGecko API（加密资产）
- 自算 PE/市值（quoteSummary 不可用时的兜底方案）

---

## 关键设计原则

- **数据可追溯**：所有数据标注来源（L1/L2/L3/L4），无来源则「未识别」
- **财务指标自算**：ROE/ROIC/PB/PE/EV 必须自算，禁止「待查」
- **年报系统遍历**：美股 Item 逐章提取，禁止只 grep 数字
- **股权激励七要素**：池总量/授予明细/归属条件/公允价值/SBC费用/波动/对价
- **扣非双口径**：大额非经常项目必须产出 GAAP + Non-GAAP 两套
- **三级信息整合**：L1(年报)→L2(券商)→L3(高临)→L4(网络兜底)

---

## 实战案例

| 标的 | 市场 | 类型 | 报告 |
|:---|:---|:---|:---|
| FUFU (BitFuFu) | 美股(海外) | 比特币挖矿 | [查看](https://github.com/panfeng0806/grit-stock-analysis) |
| CRCL (Circle Internet) | 美股(纯美国) | 稳定币/USDC | [查看](https://github.com/panfeng0806/grit-stock-analysis) |
| 安克创新 (300866) | A股 | 消费电子 | [查看](https://github.com/panfeng0806/grit-stock-analysis) |
| 携程 (09961.HK) | 港股 | OTA | [查看](https://github.com/panfeng0806/grit-stock-analysis) |

---

## 版本

**v3.3** — 纯美股完整支持 + SEC XBRL 自动转换 + 非上市竞对提取 + 三维估值 + 15 references