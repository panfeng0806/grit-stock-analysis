# 实时数据源 — 全市场

GRIT 阶段2/3 抓取实时股价、市值、加密资产价格。

---

## A 股（沪深）

### 东方财富 API — 主力

```bash
python3 -c "
import urllib.request, json
url='https://push2.eastmoney.com/api/qt/stock/get?secid=0.300866&fields=f43,f58,f116,f162,f167,f169'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
d=json.loads(urllib.request.urlopen(req,timeout=10).read())['data']
print(f'{d[\"f58\"]}: {d[\"f43\"]/100}元 | PE:{d[\"f162\"]/100:.1f} | PB:{d[\"f167\"]/100:.2f} | 市值:{d[\"f116\"]/1e8:.0f}亿')
"
```

**字段**：f43=最新价(÷100) | f58=名称 | f116=总市值(÷1e8=亿) | f162=PE-TTM(÷100) | f167=PB(÷100) | f169=涨跌幅(÷100)

secid: `0.{code}` 深市, `1.{code}` 沪市

---

## 美股（NYSE / NASDAQ）

### Yahoo Finance v8 — 主力

```bash
curl -s -H "User-Agent: Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/FUFU?interval=1d&range=5d" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['chart']['result'][0]['meta']; print(f'{d[\"regularMarketPrice\"]} | prev:{d[\"previousClose\"]}')"
```

⚠️ 必须加 `User-Agent`，否则部分 ticker 返回空。

### Financial Modeling Prep（兜底）

```bash
curl -s "https://financialmodelingprep.com/api/v3/quote/FUFU?apikey=demo"
```

免费 tier，`apikey=demo` 可偶尔使用。返回 price, marketCap, sharesOutstanding 一步到位。

### 用户 CSV

若 raw/ 中有 `股价走势.csv`（Date,Close,High,Low,Volume），取最后一行为现价——最可靠。

---

## 加密资产

### CoinGecko（免费，无需 API key）

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
```

支持 BTC/ETH/1000+ 币种。免费 tier 约 10-30 次/分钟。挖矿股（FUFU/MARA/RIOT 等）必须抓 BTC 现价。

---

## 港股（预留）

港交所 API / Yahoo Finance `.HK` 后缀。待验证。

---

## 使用规则

- **阶段2开始时** + **阶段4估值分析前** 各抓一次，确保估值基于最新行情
- 股价/PE/市值禁止用 raw 中 PDF/Excel 的历史数据
- 抓取失败则标注「数据源不可用」，而非编造
