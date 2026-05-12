# GRIT v3.4 — 框架重构版

**发布日期**：2026-05-13

---

## 概述

v3.4 是对 GRIT 框架本身的一次深度重构——不是新增功能，而是让框架更通用、更清晰、更易维护。基于 A 股 → 港股 → 美股三轮实战积累，识别出框架层面的冗余和混乱，做系统性整理。

---

## 重大变更

### 1. 路径全通用化

**问题**：SKILL.md 和 references 中大量硬编码 `/home/freddie_pan/` 路径，其他用户 clone 后无法直接使用。

**方案**：全部替换为 `${HOME}/grit/analysis/`。终端路径陷阱（Agent 的 `~` 解析为 profile home）保留在技术陷阱速查中。

### 2. 阶段编号统一

**问题**：旧版编号混乱——"阶段0→阶段1→步骤1→步骤2→步骤3→步骤4"，阶段和步骤混用，AI 执行时容易跳错。

**方案**：全部统一为「阶段N」：

```
旧                              →  新
阶段0: 项目初始化                →  阶段0: 项目初始化 (0.1-0.4)
阶段1: 扫描与覆盖                →  阶段1: 扫描与覆盖 (1.1-1.4)
步骤1: 全量文件扫描              →  阶段2: 全量文件扫描 (2.1-2.3)
步骤2: 逐线提取                  →  阶段3: 业务线逐线提取 (3.1-3.3)
步骤3: 假设溯源                  →  阶段4: 假设溯源 (4.1-4.2)
步骤4: 模板输出                  →  阶段5: 按模板输出报告 (5.1-5.2)
```

子阶段用 `0.1`、`2.2` 等编号，不再出现「步骤」一词。

### 3. 交付物规则松绑

**问题**：旧规则"单一交付物——只有 report.md"过于刚性。实战中经常需要辅助文件（如年报关键信息提取、特定行业指标表）。

**方案**：改为「主交付物为 report.md，AI 可根据项目实际情况生成辅助文件」。辅助文件用于提升分析深度的中间过程，结论必须汇总于 report.md。

### 4. Pitfall 大瘦身

**问题**：47 条 pitfalls 横跨 v1.0 到 v3.3，大量重复、过时、或已经融入正文。

**方案**：
- ~35 条融入正文对应位置（执行规则、各阶段步骤、特殊场景处理）
- ~10 条保留为「技术陷阱速查」，按场景索引（Excel/PDF/SEC/行情/路径）
- 删除 2 条重复（禁止引用 HARNESS 为独立框架、非上市竞对提取）

### 5. References 瘦身

**问题**：14 个 reference 文件，含 3 个旧版模板、1 个冗余执行引擎、2 个可合并文件。

**方案**：

```
删除（6 文件）：
  🗑 GRIT模板-v1.34.md / v1.35.md / v1.35.md.bak   旧版模板
  🗑 MASTER_HARNESS_2.0.md                          已完全吸收进 SKILL.md
  🗑 tether-competitor-extraction.md                过于特例，非通用工具
  🗑 yahoo-finance-pitfalls.md                      并入 real-time-data-sources.md
  🗑 wind-excel-structure.md                        并入 formulas.md

保留（8 文件）：
  📄 GRIT模板-v1.40.md       报告模板
  📄 real-time-data-sources   实时数据（含 Yahoo 陷阱）
  📄 formulas                 公式 + Wind Excel 提取
  📄 non-recurring-adjustment 扣非流程
  📄 special-business-models  特殊模式
  📄 market-a-share / market-us / market-hk
```

### 6. 隐私保护

所有公开文件（README、RELEASE、SKILL.md 等）移除具体股票名称、公司名称和分析报告链接。

---

## 文件变更

```
修改:
  SKILL.md                               ← v3.4，路径通用化 + 统一编号 + 规则松绑
  README.md                              ← v3.4 重写
  RELEASE.md                             ← v3.4 重写
  references/real-time-data-sources.md   ← 合并 yahoo-finance-pitfalls
  references/formulas.md                 ← 合并 wind-excel-structure（分两部分）

删除:
  references/GRIT模板-v1.34.md
  references/GRIT模板-v1.35.md
  references/GRIT模板-v1.35.md.bak
  references/MASTER_HARNESS_2.0.md
  references/tether-competitor-extraction.md
  references/yahoo-finance-pitfalls.md
  references/wind-excel-structure.md
```

---

## 向后兼容

- 所有执行流程不变（五阶段 = 旧四步骤 + 两阶段）
- A股/港股/美股分析路径无变更
- 报告模板 v1.40 未改动
- 问财 API、东方财富 API 集成不受影响

---

## 迁移指南

如果你在使用旧版 GRIT：

1. **Skill 路径**：将旧 `SKILL.md` 替换为新版，原 `~/.hermes/skills/research/grit-stock-analysis/` 路径不变
2. **分析项目路径**：新的 `${HOME}/grit/analysis/` 与旧的 `/home/freddie_pan/grit/analysis/` 功能等价
3. **辅助文件**：现在可以放心让 AI 生成辅助文件了——只要主交付物是 report.md
4. **阶段编号**：如果之前的自动化脚本引用了"步骤1-4"，对应改为"阶段2-5"
