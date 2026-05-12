# 美股市场参考（v2.0 实战提炼）

## SEC 申报文件章节导航

**每次读 20-F/10-K 时，以下章节是必读项**（不只是 grep 关键数据，而是定位到章节后完整浏览）：

| SEC 章节 | 内容 | 必读 | 提取方式 |
|:---|:---|:---:|:---|
| Item 4.A | 历史沿革 + 融资记录（SPAC/PIPE/增发/借款） | ✅ | pdftotext → 定位 "History and Development" |
| Item 5.B | 流动性 + 资本资源（ATM详情/贷款条款） | ✅ | grep "Liquidity and Capital Resources" |
| Item 6.A | 董事/高管姓名 + 完整履历 | ✅ | 定位 "ITEM 6. DIRECTORS" |
| Item 6.B | 薪酬 + **股权激励池大小、授予明细、归属条件** | ✅ | 继续往下读，含高管获授表 |
| Item 7.A | **主要股东 + 持股明细 + 投票权** | ✅ | 定位 "ITEM 7. MAJOR SHAREHOLDERS" |
| F-3 | **审计后资产负债表**（完整，含 FY2025） | ✅ | 定位 "CONSOLIDATED BALANCE SHEETS" |
| F-4 | 审计后利润表 | ✅ | 紧随 F-3 |
| F-5 | 权益变动表 | ⚠️ | 按需 |
| F-6 | 现金流量表 | ⚠️ | 按需 |
| F-7+ | 财务报表附注（SBC细节/Fair Value/关联交易/贷款） | ✅ | 搜索关键词 |

## 财务数据提取优先级

SEC 申报文件的正式报表是**文本表格**（非 HTML），grep 难以精确匹配。按以下顺序提取：

1. **6-K 新闻稿**：季度/年度业绩公告的正文以叙事形式呈现，如 "Total revenue was $475.8 million in 2025"，grep 直接命中
2. **20-F MD&A**（Item 5）：管理层讨论中会直接引用财务数字
3. **20-F 正式报表**（F-3/F-4）：最后手段，需人工逐行解析文本表格

## 实时数据源

| 数据类型 | 来源 | 方法 |
|:---|:---|:---|
| 股价/市值 | Yahoo Finance v8 | `curl -H "User-Agent: Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"` |
| BTC/ETH 价格 | CoinGecko API | `curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"` |
| 美股财务数据 | Financial Modeling Prep | `curl "https://financialmodelingprep.com/api/v3/..."`（demo key 可免费调用） |

⚠️ 东方财富 API（push2.eastmoney.com）对美股无效。

## 英文研报 OCR

```
lang='eng'  ← 不需要 chi_sim，更快更准
dpi=200
```

## 关键词中英对照

| 中文 | 英文 | grep 正则 |
|:---|:---|:---|
| 收入 | Revenue | `grep -i 'total revenue\|revenue.*\$'` |
| 净利润 | Net Income/(Loss) | `grep -i 'net.*income\|net.*loss'` |
| 毛利 | Gross Profit | `grep -i 'gross profit'` |
| 总资产 | Total Assets | `grep -i 'total assets'` |
| 股东权益 | Shareholders' Equity | `grep -i "shareholders.*equity"` |
| 股份支付 | Share-based Compensation | `grep -i 'share.based\|stock.based\|compensation expense'` |
| 目标价 | Target Price | `grep -i 'target price\|price target'` |
| 市场规模 | Market Size | `grep -i 'market size\|TAM\|addressable market'` |

## 美股特有注意事项

- PE 为负时不强行填 PE 估值，改用 EV/EBITDA、PB、P/S
- 季度数据常以 Q1/Q2/Q3/Q4 标注，FY = Fiscal Year
- 美股年报截止日不一定是 12/31（如 AAPL FY ends Sep）
- SPAC 上市公司的 Pre-IPO 融资记录在 Item 4.A
- PIPE 投资者成本 vs 现价 → 必算的稀释参照
- 认股权证（Warrants）行权价如远高于现价 → 标注"深度虚值，无现金流入"
