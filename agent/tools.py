import yfinance as yf
import pandas as pd
import pandas_ta as ta
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def get_stock_data(ticker: str, period: str = "1y") -> str:
    """获取股票基本信息、当前价格和历史数据。支持台湾股票如 2330.TW"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period=period)
        
        name = info.get("longName", ticker)
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        
        return f"""
股票：{name} ({ticker})
当前价格：{price} {info.get('currency', 'TWD')}
市值：{info.get('marketCap', 'N/A')}
52周最高/最低：{info.get('fiftyTwoWeekHigh')}/{info.get('fiftyTwoWeekLow')}
最近5日历史数据：
{hist.tail(5).to_string()}
"""
    except Exception as e:
        return f"获取 {ticker} 数据失败: {str(e)}"

@tool
def get_financials(ticker: str) -> str:
    """获取财务报表"""
    stock = yf.Ticker(ticker)
    return f"损益表：\n{stock.financials.to_string()}\n\n资产负债表：\n{stock.balance_sheet.to_string()}"

@tool
def get_technical_indicators(ticker: str) -> str:
    """计算技术指标：RSI、MACD、20日均线"""
    stock = yf.Ticker(ticker)
    df = stock.history(period="3mo")
    if df.empty:
        return "无法获取历史数据"
    df["RSI"] = ta.rsi(df["Close"], length=14)
    macd = ta.macd(df["Close"])
    df["MACD"] = macd["MACD_12_26_9"]
    df["SMA_20"] = ta.sma(df["Close"], length=20)
    return df.tail(10)[["Close", "RSI", "MACD", "SMA_20"]].round(2).to_string()

@tool
def search_financial_news(query: str) -> str:
    """搜索最新财经新闻，支持中文关键词"""
    search = TavilySearchResults(max_results=5, search_depth="advanced")
    results = search.invoke(query)
    if not results:
        return "未找到相关新闻"
    return "\n\n".join([f"标题：{r.get('title')}\n摘要：{r.get('content', '')[:300]}..." for r in results])

tools = [get_stock_data, get_financials, get_technical_indicators, search_financial_news]