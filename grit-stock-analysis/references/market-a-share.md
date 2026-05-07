# A 股市场参考

## 数据源

| 数据类型 | 来源 | 方法 |
|:---|:---|:---|
| 股价/市值/PE | 东方财富 API | `curl "https://push2.eastmoney.com/api/qt/stock/get?secid=1.600519&fields=f43,f44..."` |
| 财务数据 Excel | Wind / Choice 导出 | **Excel 优先**，年报 PDF 仅作补充 |
| 行业数据 | 问财 API | `curl -X POST "https://openapi.iwencai.com/v1/query2data" -H "Authorization: Bearer $IWENCAI_API_KEY"` |
| 年报 PDF | 巨潮资讯网 | pdftotext + grep |
| 研报 PDF | 东方财富研报中心 / 慧博 | pdftotext + grep（电子版）/ OCR（扫描版） |

## Wind/Choice Excel 行区块结构

⚠️ **切勿只读前 30 行！** 财务摘要 Excel 通常 80-90 行：

| 行范围 | 内容 | 关键指标 |
|:---:|:---|:---|
| 1-4 | 表头/日期 | — |
| 5-20 | 利润表摘要 | 收入、营业成本、三费、净利润 |
| 22-40 | 资产负债表摘要 | 总资产、总负债、股东权益 |
| 42-55 | 现金流量表摘要 | 经营/投资/筹资现金流 |
| **57-70** | **关键比率** | **ROE/ROIC/毛利率/净利率/资产负债率/周转率/现净比** |
| **72-85** | **每股指标** | **EPS/每股净资产/PE-TTM/PB/PS** |

永远用 `max_row` → `for row in ws.iter_rows(min_row=1, max_row=ws.max_row)` 读到末尾。

⚠️ Excel PE ≠ 实时 PE。Wind Excel 的 PE-TTM/PB/PS 基于导出时的股价快照，报告中使用实时 API 抓取的估值数据。

## 实时行情

东方财富 API 示例：
```bash
# A股
curl "https://push2.eastmoney.com/api/qt/stock/get?secid=1.600519&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117,f162,f167,f168,f169,f170,f171"
# 港股（如需要）
curl "https://push2.eastmoney.com/api/qt/stock/get?secid=116.00700&fields=..."
```

## 问财 API 补充（raw/ 数据不足时）

7 个可用查询维度：
- `hithink-management-query` — 前十大股东/实控人
- `hithink-business-query` — 主营构成/客户/供应商
- `hithink-industry-query` — 行业估值/排名/增速
- `hithink-finance-query` — 财务指标（ROE/负债率等）
- `hithink-event-query` — 业绩预告/重大事件
- `report-search` — 研报标题/评级
- `announcement-search` — 最新公告

财务数据优先级：**Excel > 年报 PDF > 问财 API**

## A 股特有注意事项

- 单位通常是「万元」或「亿元」，需标注并统一量纲
- 报告期标注为「YYYYMMDD」格式（如 20231231）
- 增长率计算：同比 = (当期-去年同期)/|去年同期|，环比 = (当期-上期)/|上期|
