# GRIT 五要素股票研究 Skill

> 为 [Hermes Agent](https://hermes-agent.nousresearch.com) 打造的专业股票投研技能包
>
> **当前版本：v1.5** · 2026-05-06 实战校准

---

## 这是什么？

**GRIT**（Growth · Risk · Industry · moaT · valuaTion）是一套五要素股票研究框架。它将研报级别的投研流程封装为 Hermes Agent 的一个可复用技能，让 AI 自主完成：

1. 📂 **资料索引与扫描** — 地毯式读取 Wind 财报 Excel、年报 PDF、券商研报、高临纪要
2. 🔍 **深度数据提取** — 财务追踪、业务结构、管理层、行业竞争、重大事件
3. 📊 **五要素分析** — 增长质量 / 风险矩阵 / 产业格局 / 护城河 / 估值定位
4. 📝 **结构化研报输出** — GRIT 标准模板，可追溯、可审计、无幻觉

---

## 安装

```bash
# 1. 解密（需要密码，联系分享者获取）
age -d grit-v1.5.tar.gz.age | tar xz

# 2. 安装到 Hermes
hermes skill install grit-stock-analysis/

# 3. 首次使用需安装 openpyxl（用于读取 Wind Excel）
pip install openpyxl --break-system-packages
```

> **依赖**：需要安装 `pdftotext`（apt install poppler-utils），用于提取 PDF 中的券商研报文本。

---

## 使用

在 Hermes Agent 对话中直接说：

```
分析一下安克创新 300866
跑一下 GRIT 格力电器
帮我看看宁德时代
```

AI 会按以下阶段推进：

| 阶段 | 步骤 | 说明 |
|:---|:---|:---|
| 0 | 创建文件夹 + 输出资料清单 | 告诉你要准备哪些资料 |
| 1 | 用户放入 raw/ → 扫描 | 生成覆盖-缺口矩阵 |
| 2 | 全部阅读 + 结构化提取 | 产出 extracted.md |
| 3 | 构建五要素分析 | 核心分析段落 |
| 4 | 生成完整报告 | report.md |
| 5 | 全面质量校验 | 6 大类 20+ 检查项 |

> 完整交互协议见 SKILL.md →「交互模式速查」。

---

## 你需要准备的原始资料

放入 `raw/` 文件夹：

```
raw/
├── Wind财务摘要.xlsx          # Wind/Choice 导出的财务Excel
├── 竞争对手/
│   ├── 绿联科技.xlsx           # 可比公司Wind Excel
│   └── 传音控股.xlsx
├── 年报/
│   ├── 2024年报.pdf
│   └── 2025年报.pdf
├── 券商研报/                   # 支持中英文PDF
│   ├── 信达证券-深度报告.pdf
│   └── UBS-Company_Note.pdf
├── 高临纪要/                   # 行业专家访谈
└── 问财-行业数据.txt            # 可选：问财OpenAPI数据
```

>  没有券商研报也能跑，但深度会打折扣。最少需要 **Wind 财务摘要 Excel**。

---

## v1.5 重大更新（2026-05-06）

基于安克创新（300866.SZ）全流程实战校准，新增 7 条硬约束：

| # | 规则 | 解决的问题 |
|:---:|:---|:---|
| 14 | 禁止删除模板任何维度 | 「净利环比」被无故删除 |
| 15 | PE-TTM 自算且全文唯一 | 报告出现 34.97/23.81/25.9 三个矛盾值 |
| 16 | 推算 > 提取 > 标注 > 「未识别」 | 期间费用率明明可推算却被标「未识别」 |
| 17 | EPS/市值统一量纲 | 券商预测用 EPS，内部用市值，无法对话 |
| 18 | 增长类型全量罗列 | 只列匹配的，遗漏减速信号 |
| 19 | 季度表必须覆盖最新报告期 | Q1 2026 季报被忽略 |
| 20 | 支持问财 OpenAPI 补充 | 管理层/行业数据可从问财实时获取 |

> 完整 changelog 见 SKILL.md 末尾 Pitfalls 14-20。

---

## 技术细节

### 核心文件

```
grit-stock-analysis/
├── SKILL.md                                    # 主技能文件（Agent 行为定义）
└── references/
    ├── GRIT模板-五要素股票AI研究提示词-v1.34.md   # 报告模板
    ├── HARNESS-股票研究执行框架-v1.34.md          # 执行框架
    ├── wind-excel-structure.md                  # Wind Excel 行号映射
    └── real-time-data-sources.md                # 实时数据源（股价/估值）
```

### 防止幻觉的关键设计

- **单向流水线**：raw → extracted → report，禁止跳过中间步骤
- **原始引用可追溯**：所有数据标注来源文件、行号、时点
- **缺失显式标注**：无数据标「未识别」而非编造（v1.5 后改为「推算值」优先）
- **20 条硬约束**：从实战踩坑提炼的不可违反规则

---

## FAQ

**Q: 为什么加密分发？**
A: 这是专业投研工具，限内部使用。加密确保只有授权人员可以获取。

**Q: 支持 A 股以外的市场吗？**
A: 当前框架为 A 股设计（Wind 财务 Excel 格式），港股/美股需要适配数据源格式。

**Q: 对 AI 模型有要求吗？**
A: 需要具备 128K+ 上下文窗口的模型（报告常达 800+ 行）。推荐 Claude Sonnet 4、DeepSeek V3/R1。

**Q: 没有 Wind 账号怎么办？**
A: 可以手工作一份 CSV（收入/成本/利润/现金流/关键比率），放入 raw/ 即可。

---

## License

内部使用 · 禁止外传

---

<p align="center">
  <sub>Built with Hermes Agent · GRIT Framework v1.5</sub>
</p>
