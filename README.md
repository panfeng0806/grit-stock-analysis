# GRIT 五要素股票研究 v3.4

> AI Agent 通用投研技能包 — 让任何 AI Agent 都能产出研报级别的股票分析

---

## 概述

GRIT 是一个结构化的股票投研流程框架，将「原始资料 → 结构化素材 → 深度分析 → 完整报告」串成单向流水线。它不是财务数据查询工具——它是一套让 AI Agent 像分析师一样思考的认知流程。

**五要素**：需求、竞争、资本、估值、风险。

**v3.4 核心改进**：框架重构——路径全通用化、阶段编号统一、pitfall 从 47 条精简融入正文、references 从 14 文件瘦身至 8 文件。

---

## 适用市场

| 市场 | 判定依据 | 数据源 |
|:---|:---|:---|
| A 股 | 代码纯数字 / 用户指定 | Wind/Choice Excel、东方财富 API、问财 API、巨潮资讯网 |
| 美股 | 代码含字母 / raw 中有 10-K/10-Q/424B4 | SEC EDGAR（XBRL 自动转换）、Yahoo Finance v8 |
| 港股 | 代码 5 位数字 / .HK 后缀 | 港交所披露易、Yahoo Finance v8、Wind Excel |

阶段 0 自动检测市场，加载对应参考文件。

---

## 工作流程

```
阶段0: 项目初始化（市场检测 → 创建文件夹 → 输出资料清单）
阶段1: 扫描与覆盖评估（扫描 raw/ → 覆盖-缺口矩阵 → 用户决策）
══════════════════════════════════════════════ ← 用户交互线
阶段2: 全量文件扫描（预检 → 格式转换 → 逐文件标注）
阶段3: 业务线逐线提取（B1-B7 七类信息）
阶段4: 假设溯源（来源链 + 推导 + 置信度）
阶段5: 按 GRIT 模板 v1.40 输出报告
══════════════════════════════════════════════
输出前自检
```

---

## 文件结构

```
grit-stock-analysis/
├── SKILL.md                              ← 核心流程（自包含所有执行规则）
├── references/
│   ├── GRIT模板-v1.40.md                 ← 报告模板（三级信息整合 + IC卡）
│   ├── real-time-data-sources.md         ← 全市场实时数据源（含Yahoo API陷阱）
│   ├── market-a-share.md                 ← A股：Wind Excel / 东方财富 / 问财
│   ├── market-us.md                      ← 美股：SEC章节导航 / 10-K提取
│   ├── market-hk.md                      ← 港股：港交所披露易 / Wind Excel
│   ├── formulas.md                       ← 衍生指标计算 + Wind Excel数据提取
│   ├── non-recurring-adjustment.md       ← 非经常性损益剔除流程
│   └── special-business-models.md        ← 特殊商业模式处理
└── tools/
    └── sec_xbrl_to_text.py               ← SEC iXBRL HTML → 纯文本转换器
```

---

## 安装

GRIT 不依赖任何特定 Agent——**它就是一堆 Markdown 文件**。放到你 AI Agent 加载 skills / context documents 的目录下即可。

| Agent | 放置位置 |
|:---|:---|
| Hermes | `~/.hermes/skills/research/grit-stock-analysis/` |
| Claude Code | 项目 `.claude/commands/` 或通过 CLAUDE.md 引用 |
| Cursor | 项目根目录，通过 `.cursorrules` 引用 |
| 其他 | 任何 Agent 能读取到的路径即可 |

```bash
git clone https://github.com/panfeng0806/grit-stock-analysis.git /你的/skills/目录/grit-stock-analysis
```

---

## 使用方式

1. 将标的原始资料（年报 PDF/HTML、财务 Excel、券商研报、调研纪要等）放入 `raw/` 文件夹
2. 对 Agent 说：「分析一下 XXX（代码 XXX）」
3. Agent 自动执行五阶段流程，产出完整报告

**输出**：

```
~/grit/analysis/{股票名称}（{股票代码}）/
├── raw/             ← 原始资料
└── report.md        ← 完整 GRIT 报告（主交付物）
```

---

## 核心能力

### 跨市场支持
- **A 股**：Wind/Choice Excel、东方财富 API、问财 API
- **美股**：SEC EDGAR（自动识别 iXBRL 并转换为纯文本）、Yahoo Finance v8 chart
- **港股**：港交所披露易、Yahoo Finance v8、Wind Excel（含币种/汇率处理）

### 执行规则（6 条贯穿全程）
- **来源链随行**：每个数据点携带 (Lx|文件|位置) 标注
- **三级信息整合**：L1(年报)→L2(券商)→L3(高临)→L4(网络兜底)
- **假设溯源**：盈利预测每项假设对应完整推导链 + 置信度
- **按业务线过滤**：不同业务线数据严格分离
- **允许合理推算，禁止编造**：【直接】/【推算】/【推断】三级置信度
- **主交付物 + 按需辅助**：report.md 为主，AI 可按需生成辅助文件

### SEC 申报文件自动化
- iXBRL HTML 自动剥离 XBRL 标签 → 纯文本
- 10-K/10-Q/424B4/S-1 全章节遍历（Item 1-16）
- 财务数据优先 Excel，parsed 文本用于叙事章节

### 财务深度
- ROE/ROIC/PB/PE/EV/EBITDA 全部自算，禁止「待查」
- 股权激励七要素强制提取
- 融资历史完整表格（含 PIPE 成本 vs 现价稀释）
- 大额非经常项目自动识别 + GAAP/扣非双口径产出

---

## 关键设计原则

- **数据可追溯**：所有数据标注来源，无来源则「未识别」
- **年报系统遍历**：年报逐 Item 提取，禁止只 grep 数字
- **股权激励深度**：池总量/授予明细/归属条件/公允价值/SBC/波动/对价
- **扣非双口径**：大额非经常项目必须产出 GAAP + Non-GAAP 两套
- **三级信息整合**：L1→L2→L3→L4 逐级降置信度
- **路径通用化**：`${HOME}/grit/analysis/`，无硬编码用户名

---

## 版本历史

| 版本 | 日期 | 关键变更 |
|:---|:---|:---|
| v3.4 | 2026-05 | 框架重构：路径通用化、阶段统一编号、pitfall 精简融入、references 瘦身 14→8 |
| v3.3 | 2026-05 | 纯美股支持：SEC XBRL 自动转换、特殊商业模式框架、Yahoo v8 验证 |
| v3.2 | 2026-04 | 港股实战：港交所年报提取、扣非七步流程、问财 API 集成 |
| v2.0 | 2026-03 | HARNESS 执行引擎：全量扫描→逐线提取→假设溯源→模板输出 |
| v1.0 | 2026-02 | 初始版本：A 股实战验证 |
