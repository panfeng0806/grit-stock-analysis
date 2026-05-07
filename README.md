# GRIT 五要素股票研究

> AI Agent 通用投研技能包 — 让任何 AI Agent 都能产出研报级别的股票分析

---

## 概述

GRIT 是一个结构化的股票投研流程框架，将「原始资料 → 结构化素材 → 深度分析 → 完整报告」串成一条单向流水线。它不是财务数据查询工具——它是一套让 AI Agent 像分析师一样思考的认知流程。

**五要素**：需求、竞争、资本、估值、风险。

---

## 适用市场

| 市场 | 判定依据 | 数据源 |
|:---|:---|:---|
| A 股 | 代码纯数字 / 用户指定 | Wind/Choice Excel、东方财富 API、问财 API、巨潮资讯网 |
| 美股 | 代码含字母 / raw 中有 20-F/10-K | SEC EDGAR、Yahoo Finance、CoinGecko、Seeking Alpha |
| 港股 | 代码 5 位数字 / .HK 后缀 | 港交所披露易（预留扩展） |

阶段 0 自动检测市场，加载对应参考文件。不同市场共享同一框架，差异仅在于数据源和提取方式。

---

## 工作流程

```
阶段0: 项目初始化（市场检测 → 创建文件夹 → 输出资料清单）
阶段1: Task 理解（扫描 raw/ → 覆盖-缺口矩阵 → 询问用户是否补资料）
阶段2: 全量检索（无一遗漏地毯式扫描 → 财务数据推算 → 缺口二次确认）
阶段3: 信息提取（→ extracted.md：结构化素材层，按业务线/管理层/财务/行业/竞争/估值/风险分离）
阶段4: 深度分析（逐业务产业逻辑 → 季度财务 → 产业全景 → 五要素归纳）
阶段5: 报告生成（→ report.md：严格按 GRIT 模板格式输出）
阶段6: 质量校验（数据追溯/深度分析/跨引用一致性/延伸关注/完整性 → sources.md）
```

---

## 文件结构

```
grit-stock-analysis/
├── SKILL.md                          ← 核心流程（自包含所有执行规则）
└── references/
    ├── GRIT模板-五要素股票AI研究提示词-v1.35.md ← 报告模板
    ├── real-time-data-sources.md      ← 全市场实时数据源（A股/美股/加密）
    ├── market-a-share.md              ← A股：Wind Excel / 东方财富 / 问财
    ├── market-us.md                   ← 美股：SEC章节导航 / 20-F提取 / Yahoo Finance
    ├── formulas.md                    ← 衍生指标自动计算公式
    ├── wind-excel-structure.md        ← Wind/Choice Excel 行区块结构
    └── (v1.34 旧模板保留)
```

---

## 安装

GRIT 不依赖任何特定 Agent——**它就是一堆 Markdown 文件**。放到你 AI Agent 加载 skills / context documents 的目录下即可。

常见的 Agent 对应路径：

| Agent | 放置位置 |
|:---|:---|
| Hermes | `~/.hermes/skills/research/grit-stock-analysis/` |
| OpenClaw | 项目根目录或自定义 skills 文件夹 |
| Claude Code | 项目 `.claude/commands/` 或通过 CLAUDE.md 引用 |
| Cursor | 项目根目录，通过 `.cursorrules` 引用 |
| 其他 | 任何 Agent 能读取到的路径即可 |

下载方式二选一：

```bash
# 方式一：从 GitHub Releases 下载 ZIP
# 解压后将 grit-stock-analysis/ 放到你的 Agent skills 目录

# 方式二：git clone（推荐，方便后续更新）
git clone https://github.com/panfeng0806/grit-stock-analysis.git /你的/skills/目录/grit-stock-analysis
```

## 使用方式

1. 将标的原始资料（年报 PDF、财务 Excel、券商研报、调研纪要等）放入 `raw/` 文件夹
2. 对 Agent 说：「分析一下 XXX（代码 XXX）」
3. Agent 自动执行六阶段流程，产出结构化素材 + 完整报告 + 数据来源清单

**输出**：

```
~/grit/analysis/{股票名称}（{股票代码}）/
├── raw/             ← 原始资料
├── extracted.md     ← 结构化素材层
├── report.md        ← 完整 GRIT 报告
└── sources.md       ← 数据来源清单
```

---

## 关键设计原则

### 数据可追溯
所有数据标注来源（精确到文件+行号/单元格），无来源则标注「未识别」，严禁编造。

### OCR 兜底
电子版 PDF 用 pdftotext，扫描版 PDF 自动切换到 tesseract OCR。OCR 仅用于 pdftotext 失败后。

### 财务指标自算
禁止在可推算的情况下标注「待查」。ROE、PB、EV/EBITDA、Q4 季度数据等衍生指标必须自动计算。

### 年报系统遍历
美股 20-F/10-K 必须逐章提取：融资史（Item 4）→ 高管（Item 6）→ 股东（Item 7）→ 资产负债表（F-3）→ 利润表（F-4）。禁止只 grep 财务数字就认为「年报已读完」。

### 股权激励七要素
激励池总量、已授予/归属/作废分拆、高管明细、归属条件、公允价值、SBC 费用波动、获授对价——七项缺一不可。

### 融资历史完整表
所有融资事件（SPAC/IPO/PIPE/增发/抵押贷款等）纳入表格，PIPE 成本 vs 现价稀释幅度必算。

---

## 版本

**v2.2** — 自包含 SKILL.md，统一全市场数据源，8 文件精简架构。
