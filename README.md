# GRIT 五要素股票研究

> AI Agent 通用投研技能包 — 让任何 AI Agent 都能产出研报级别的股票分析
>
> **v1.7** · 2026-05-07 问财API补充查询 + 实时行情抓取时机固化 · 安克创新 300866.SZ 全流程验证

---

## 这是什么

**GRIT**（Growth · Risk · Industry · moaT · valuaTion）是一套五要素股票研究框架。它本质上是一个**给 AI Agent 看的提示词工程包**——定义了一套 agent 在分析股票时必须遵循的方法论、数据流和硬约束。

它不是脚本，不是 API，是一个 **Skill**：告诉 AI Agent 怎么读资料、怎么推理、怎么写报告。

### AI Agent 拿到它之后能干什么

1. 扫描 `raw/` 文件夹里的 Wind 财务 Excel、年报 PDF、券商研报、行业纪要
2. 地毯式提取结构化数据，生成 `extracted.md`
3. 按五要素（增长/风险/产业/护城河/估值）逐一深度分析
4. 输出一份可追溯、无幻觉、格式统一的研报级 `report.md`

---

## 适用平台

这不是某个特定 agent 的插件。只要 AI agent **能读文件 + 能执行命令**，它就能用 GRIT：

| 平台 | 用法 |
|:---|:---|
| [Hermes Agent](https://hermes-agent.nousresearch.com) | `hermes skill install grit-stock-analysis/` |
| [OpenClaw](https://github.com/nicholasgriffintn/openclaw) | 放入 workspace skills 目录 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | 放入 `.claude/skills/` 或直接 `/add-dir` |
| [OpenAI Codex](https://github.com/openai/codex) | 放入项目 `.codex/skills/` |
| [OpenCode](https://github.com/sst/opencode) | 放入 workspace，prompt 中引用 |
| 任何通用 LLM Agent | 把 SKILL.md + references 作为 system prompt 注入 |

> 核心交互协议在各平台都一样：agent 看到「分析 XXX 股票」→ 加载 GRIT skill → 走 6 阶段流水线。

---

## 快速开始

```bash
# 1. 解密（需要密码）
age -d grit-v1.7.tar.gz.age | tar xz

# 2. 放入你的 AI Agent 的 skills/workspace 目录
cp -r grit-stock-analysis/ ~/.hermes/skills/research/     # Hermes
# 或
cp -r grit-stock-analysis/ ~/.openclaw/skills/             # OpenClaw
# 或
cp -r grit-stock-analysis/ ~/.claude/skills/               # Claude Code
# 或任何你的 agent 读取 skill 的路径

# 3. 安装 pdftotext（几乎所有平台的 agent 都用到）
# macOS:  brew install poppler
# Linux:  apt install poppler-utils
# Win:    https://github.com/oschwartz10612/poppler-windows

# 4. 如果 raw/ 里有 Excel，agent 首次运行时需安装
pip install openpyxl --break-system-packages
```

---

## 你需要准备的资料

扔进 `raw/` 文件夹：

```
raw/
├── Wind财务摘要.xlsx          #   Wind/Choice 导出的财务数据
├── 竞争对手/
│   ├── 绿联科技.xlsx           # 可比公司（用于估值对比）
│   └── ...
├── 年报/
│   ├── 2024年报.pdf
│   └── 2025年报.pdf            # 最新年度报告
├── 季报/
│   └── 2026Q1报告.pdf          # 有最新季报务必放入
├── 券商研报/                   # 中英文 PDF 都支持
│   ├── 信达证券-深度报告.pdf
│   └── UBS-Company_Note.pdf
├── 高临纪要/                   # 专家访谈、行业会议纪要
└── 问财-行业数据.txt            # 可选：同花顺问财 OpenAPI 数据
```

> 最少需要一份 **Wind 财务摘要 Excel**。资料越全，报告越深。

---

## 交互流程

Agent 拿到这个 skill 后会按 6 个阶段走：

| 阶段 | 做什么 | 产出 |
|:---|:---|:---|
| 0 | 创建文件夹 + 输出资料需求清单 | 告诉你要准备什么 |
| 1 | 扫描 raw/，生成覆盖-缺口矩阵 | 让你知道缺什么 |
| 2 | 全量读取所有文件，结构化提取 | `extracted.md` |
| 3 | 构建五要素分析段落 | 核心分析 |
| 4 | 拼接 GRIT 标准模板 | `report.md` |
| 5 | 6 大类 20+ 项质量校验 | 无遗漏、无矛盾 |
| 6 | 最终交付 | 完整研报 + 数据来源清单 |

---

## v1.7 更新（2026-05-07）

- **GRIT 模板升级至 v1.35**：新增「管理层与股权结构」板块（前十大股东、核心高管、股权激励）
- **HARNESS 框架升级至 v1.35**：新增管理层素材 checklist + extracted.md 结构扩展
- **新增 Pitfall #20**：raw 数据不足时主动调用问财 API 补充（7 个查询维度）
- **新增「维度四：问财 API 补充」**：阶段 2 检索策略中加入问财 OpenAPI 调用指导
- **实时行情抓取时机固化**：阶段 2 开始时 + 阶段 4 估值分析前各抓一次
- 安克创新 300866.SZ 实战验证通过

## v1.6 更新（2026-05-07）

- 清理重复 pitfall（#16 和末尾重复条目合并）
- 修正 README 版本号

## v1.5 更新（2026-05-06）

基于安克创新 300866.SZ 全流程实战后的校准。

**核心教训：三个字——偷懒、不统一、不推算**

| # | 硬约束 | 踩过的坑 |
|:---:|:---|:---|
| 14 | 禁止删除模板任何维度 | 季度表莫名少了「净利环比」行 |
| 15 | PE-TTM 必须自算且全文唯一 | 报告出现 34.97 / 23.81 / 25.9 三个矛盾值 |
| 16 | 推算 > 提取 > 标注 > 最后才「未识别」 | 期间费用率明明可算却标未识别 |
| 17 | EPS 与市值统一量纲 | 券商预测 EPS，内部算市值，无法对话 |
| 18 | 增长类型全量罗列 | AI 自作主张只列匹配的，掩盖了减速信号 |
| 19 | 季度表必须覆盖最新报告期 | Q1 2026 季报静静躺在 raw 里被忽略了 |
| 20 | 支持问财 OpenAPI 补充查询 | 管理层/行业数据 raw 里没有，但 API 有 |

> 完整细则见 `grit-stock-analysis/SKILL.md` 末尾 Pitfalls 14-20。

---

## 文件结构

```
grit-stock-analysis/
├── SKILL.md                                    # 主文件：Agent 行为全定义
└── references/
    ├── GRIT模板-...-v1.35.md                    # 研报标准模板
    ├── HARNESS-...-v1.35.md                     # 执行框架（6阶段流水线）
    ├── wind-excel-structure.md                  # Wind Excel 行号映射（别漏关键比率）
    └── real-time-data-sources.md                # 实时股价/估值数据源
```

---

## 设计原则

**「不是给 AI 编规则，是让 AI 学会像分析师一样思考」**

- **单向流水线**：raw → extracted → report，跳过任何步骤都会导致幻觉
- **数据可追溯**：每个数字标注来源文件、行号、时点
- **缺则标注**：无数据标「未识别」或「推算值」，绝不编造
- **硬约束优先**：20 条从实战踩坑提炼的不可违反规则，优先级高于 AI 的自主判断
- **平台无关**：任何能读文件 + 执行命令的 AI Agent 都能用

---

## FAQ

**Q: 为什么加密分发？**
A: 专业投研工具，限授权人员使用。

**Q: 需要什么 AI 模型？**
A: 推荐 128K+ 上下文窗口（报告常达 800+ 行）。Claude Sonnet 4、Gemini 2.5 Pro、DeepSeek V3/R1 都跑过，没问题。

**Q: 需要问财 API 吗？不配能跑吗？**
A: 不必须。raw/ 里资料够全就能跑完。但如果有 `IWENCAI_API_KEY`，agent 会自动补充管理层/行业/研报数据（详见 `iwencai-setup` skill 配置指南）。配置方法：`export IWENCAI_API_KEY=<key>`，开通地址：https://www.iwencai.com/skillhub。

**Q: 没有 Wind 账号怎么办？**
A: 手工整理一份 CSV（营收/成本/利润/现金流/关键比率），格式对齐 Wind 导出行号即可。

**Q: 能用于港股/美股吗？**
A: 框架是市场无关的，但 references 里的 Excel 行号映射是为 A 股 Wind 格式写的。港股/美股需要适配数据源格式。

---

## License

内部授权使用 · 禁止外传

---

<p align="center">
  <sub>Agent-agnostic · GRIT Framework v1.7 · 2026</sub>
</p>
