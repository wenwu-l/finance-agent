import time
import random
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults   # 使用这个导入

# ==================== 简单缓存 ====================
_cache = {}

def _cached_ticker(ticker: str):
    if ticker not in _cache:
        _cache[ticker] = yf.Ticker(ticker)
    return _cache[ticker]

@tool
def get_stock_data(ticker: str, period: str = "1y") -> str:
    """获取股票基本信息、当前价格和历史数据。支持台湾股票如 2330.TW"""
    for attempt in range(5):
        try:
            stock = _cached_ticker(ticker)
            info = stock.info
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError("历史数据为空")
                
            name = info.get("longName", ticker)
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            
            return f"""
股票：{name} ({ticker})
当前价格：{price} {info.get('currency', 'TWD')}
市值：{info.get('marketCap', 'N/A')}
52周最高/最低：{info.get('fiftyTwoWeekHigh')}/{info.get('fiftyTwoWeekLow')}
最近5日数据：
{hist.tail(5).to_string()}
"""
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "too many requests" in error_str or "429" in error_str:
                wait = 8 + attempt * 5 + random.uniform(0, 3)
                print(f"yfinance 限流，正在等待 {wait:.1f} 秒... ({attempt+1}/5)")
                time.sleep(wait)
            else:
                return f"获取 {ticker} 数据失败: {str(e)}"
    
    return f"获取 {ticker} 数据失败：多次尝试后仍被限流，请等待几分钟后再试。"

@tool
def get_financials(ticker: str) -> str:
    """获取财务报表"""
    try:
        stock = _cached_ticker(ticker)
        financials = stock.financials.to_string() if not stock.financials.empty else "无损益表数据"
        balance = stock.balance_sheet.to_string() if not stock.balance_sheet.empty else "无资产负债表数据"
        return f"损益表：\n{financials}\n\n资产负债表：\n{balance}"
    except Exception as e:
        return f"获取财务报表失败: {str(e)}"

@tool
def get_technical_indicators(ticker: str) -> str:
    """计算技术指标"""
    for attempt in range(4):
        try:
            stock = _cached_ticker(ticker)
            df = stock.history(period="3mo")
            if df.empty:
                return "无法获取历史数据"
            df["RSI"] = ta.rsi(df["Close"], length=14)
            macd = ta.macd(df["Close"])
            df["MACD"] = macd["MACD_12_26_9"]
            df["SMA_20"] = ta.sma(df["Close"], length=20)
            return df.tail(10)[["Close", "RSI", "MACD", "SMA_20"]].round(2).to_string()
        except Exception as e:
            if "rate limit" in str(e).lower() or "too many" in str(e).lower():
                time.sleep(6 + attempt * 4)
            else:
                return f"计算技术指标失败: {str(e)}"
    return "技术指标获取失败：限流严重，请稍后重试"

@tool
def search_financial_news(query: str) -> str:
    """搜索最新财经新闻"""
    search = TavilySearchResults(max_results=5, search_depth="advanced")
    results = search.invoke(query)
    if not results:
        return "未找到相关新闻"
    return "\n\n".join([f"标题：{r.get('title')}\n摘要：{r.get('content', '')[:300]}..." for r in results])

tools = [get_stock_data, get_financials, get_technical_indicators, search_financial_news]