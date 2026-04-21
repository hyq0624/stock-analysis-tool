"""
Interactive Stock Market Analysis Tool
A Streamlit-based application for analyzing and comparing tech company stock performance.
Author: ACC102 Student
Date: April 2026
"""

import os
import time
import random
import warnings
from datetime import datetime, timedelta

# ── 清除所有代理环境变量（必须在其他 import 之前）──────────────────────────────
for _k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"]:
    os.environ.pop(_k, None)

import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Stock Market Analysis Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Interactive Stock Market Analysis Tool")
st.markdown(
    "This tool provides analysis of major tech company stocks, including price trends, "
    "technical indicators, and comparative performance metrics."
)

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.header("Configuration")

COMPANIES = {
    "Apple":     "AAPL",
    "Microsoft": "MSFT",
    "Tesla":     "TSLA",
    "NVIDIA":    "NVDA",
    "Amazon":    "AMZN",
    "Google":    "GOOGL",
    "Meta":      "META",
    "Intel":     "INTC",
}

selected_companies = st.sidebar.multiselect(
    "Select companies to analyze:",
    options=list(COMPANIES.keys()),
    default=["Apple", "Microsoft", "Tesla"],
)

date_range = st.sidebar.selectbox(
    "Select time period:",
    options=["1 Month", "3 Months", "6 Months", "1 Year", "2 Years"],
    index=2,
)

DATE_MAP = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365, "2 Years": 730}
days       = DATE_MAP[date_range]
end_date   = datetime.now()
start_date = end_date - timedelta(days=days)

st.sidebar.header("Technical Indicators")
show_ma20   = st.sidebar.checkbox("Show 20-day Moving Average", value=True)
show_ma50   = st.sidebar.checkbox("Show 50-day Moving Average", value=True)
show_volume = st.sidebar.checkbox("Show Trading Volume",        value=True)

# ============================================================================
# DATA FETCHING  ── 3 个数据源，依次尝试
# ============================================================================

def _fetch_via_stooq(ticker: str, start: datetime, end: datetime) -> pd.DataFrame | None:
    """Stooq CSV — no API key needed, very reliable from cloud."""
    url = (
        f"https://stooq.com/q/d/l/?s={ticker.lower()}.us"
        f"&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d"
    )
    try:
        resp = requests.get(url, timeout=15,
                            headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200 or len(resp.text) < 50:
            return None
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), parse_dates=["Date"], index_col="Date")
        df.columns = [c.strip().capitalize() for c in df.columns]
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
        df.sort_index(inplace=True)
        return df if not df.empty else None
    except Exception:
        return None


def _fetch_via_yahoo_query(ticker: str, start: datetime, end: datetime) -> pd.DataFrame | None:
    """Yahoo Finance v8 JSON endpoint — direct, no yfinance library."""
    p1, p2 = int(start.timestamp()), int(end.timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval=1d&period1={p1}&period2={p2}&includePrePost=false"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None
        js = resp.json()
        result = js["chart"]["result"]
        if not result:
            return None
        r         = result[0]
        timestamps = r["timestamp"]
        ohlcv      = r["indicators"]["quote"][0]
        adj_close  = r["indicators"].get("adjclose", [{}])[0].get("adjclose", ohlcv["close"])

        dates  = pd.to_datetime(timestamps, unit="s", utc=True).tz_convert("America/New_York").normalize()
        df = pd.DataFrame({
            "Open":   ohlcv["open"],
            "High":   ohlcv["high"],
            "Low":    ohlcv["low"],
            "Close":  adj_close,
            "Volume": ohlcv["volume"],
        }, index=dates)
        df.index.name = "Date"
        df = df.dropna(subset=["Close"]).sort_index()
        return df if not df.empty else None
    except Exception:
        return None


def _fetch_via_yahoo_v7(ticker: str, start: datetime, end: datetime) -> pd.DataFrame | None:
    """Yahoo Finance v7 download endpoint — fallback."""
    p1, p2 = int(start.timestamp()), int(end.timestamp())
    url = (
        f"https://query2.finance.yahoo.com/v7/finance/download/{ticker}"
        f"?period1={p1}&period2={p2}&interval=1d&events=history&includeAdjustedClose=true"
    )
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200 or "Date" not in resp.text[:50]:
            return None
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), parse_dates=["Date"], index_col="Date")
        df.columns = [c.strip() for c in df.columns]
        if "Adj Close" in df.columns:
            df["Close"] = df["Adj Close"]
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
        df.sort_index(inplace=True)
        return df if not df.empty else None
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_data(ticker: str, start: datetime, end: datetime) -> pd.DataFrame | None:
    """
    Try 3 data sources in order:
      1. Stooq (most reliable on Streamlit Cloud)
      2. Yahoo Finance v8 JSON
      3. Yahoo Finance v7 CSV
    """
    fetchers = [
        ("Stooq",         _fetch_via_stooq),
        ("Yahoo v8 JSON", _fetch_via_yahoo_query),
        ("Yahoo v7 CSV",  _fetch_via_yahoo_v7),
    ]
    for name, fn in fetchers:
        try:
            df = fn(ticker, start, end)
            if df is not None and not df.empty:
                return df
        except Exception:
            pass
        time.sleep(random.uniform(0.3, 0.8))

    return None


# ============================================================================
# HELPERS
# ============================================================================

def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    return df


@st.cache_data(show_spinner=False)
def calculate_metrics(df: pd.DataFrame) -> dict | None:
    if df is None or df.empty:
        return None
    cur  = float(df["Close"].iloc[-1])
    prev = float(df["Close"].iloc[0])
    chg  = cur - prev
    return {
        "current_price":    cur,
        "price_change":     chg,
        "price_change_pct": chg / prev * 100,
        "high_52w":         float(df["Close"].max()),
        "low_52w":          float(df["Close"].min()),
        "avg_volume":       float(df["Volume"].mean()),
    }


# ============================================================================
# MAIN
# ============================================================================

if not selected_companies:
    st.info("👈 Please select at least one company from the sidebar to begin analysis.")
    st.stop()

stock_data: dict[str, pd.DataFrame] = {}
metrics_data: dict[str, dict] = {}

progress = st.progress(0, text="正在获取股票数据，请稍候...")
total = len(selected_companies)

for i, company in enumerate(selected_companies):
    ticker = COMPANIES[company]
    progress.progress((i) / total, text=f"正在获取 {company} ({ticker}) 的数据…")
    df = fetch_stock_data(ticker, start_date, end_date)
    if df is not None:
        df = add_moving_averages(df)
        stock_data[company]   = df
        metrics_data[company] = calculate_metrics(df)
    else:
        st.warning(f"⚠️ 无法获取 **{company}** 的数据，已跳过。")
    time.sleep(random.uniform(0.2, 0.6))

progress.progress(1.0, text="数据加载完成 ✅")
time.sleep(0.5)
progress.empty()

if not stock_data:
    st.error("❌ 所有股票数据均获取失败，请稍后刷新重试。")
    st.stop()

# ── KEY METRICS ──────────────────────────────────────────────────────────────
st.header("Key Metrics")
cols = st.columns(len(stock_data))
for idx, company in enumerate(stock_data):
    m = metrics_data.get(company)
    if not m:
        continue
    with cols[idx]:
        st.subheader(company)
        color = "normal" if m["price_change"] >= 0 else "inverse"
        st.metric(
            "Current Price",
            f"${m['current_price']:.2f}",
            f"{m['price_change']:+.2f} ({m['price_change_pct']:+.2f}%)",
        )
        c1, c2 = st.columns(2)
        c1.metric("52W High", f"${m['high_52w']:.2f}")
        c2.metric("52W Low",  f"${m['low_52w']:.2f}")

# ── PRICE TREND ──────────────────────────────────────────────────────────────
st.header("Price Trend Analysis")
fig_price = go.Figure()
for company, df in stock_data.items():
    fig_price.add_trace(go.Scatter(
        x=df.index, y=df["Close"], mode="lines", name=company,
        hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>",
    ))
    if show_ma20 and "MA20" in df.columns:
        fig_price.add_trace(go.Scatter(
            x=df.index, y=df["MA20"], mode="lines",
            name=f"{company} MA20", line=dict(dash="dash", width=1), opacity=0.5,
            hovertemplate="<b>%{fullData.name} MA20</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>",
        ))
    if show_ma50 and "MA50" in df.columns:
        fig_price.add_trace(go.Scatter(
            x=df.index, y=df["MA50"], mode="lines",
            name=f"{company} MA50", line=dict(dash="dot", width=1), opacity=0.5,
            hovertemplate="<b>%{fullData.name} MA50</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>",
        ))
fig_price.update_layout(
    title=f"Stock Price Trends ({date_range})",
    xaxis_title="Date", yaxis_title="Price (USD)",
    hovermode="x unified", height=500, template="plotly_white",
)
st.plotly_chart(fig_price, use_container_width=True)

# ── NORMALISED PERFORMANCE ────────────────────────────────────────────────────
st.header("Performance Comparison (Normalized)")
fig_norm = go.Figure()
for company, df in stock_data.items():
    norm = df["Close"] / float(df["Close"].iloc[0]) * 100
    fig_norm.add_trace(go.Scatter(
        x=norm.index, y=norm, mode="lines", name=company,
        hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>%{y:.2f}<extra></extra>",
    ))
fig_norm.update_layout(
    title="Normalized Price Performance (Base = 100)",
    xaxis_title="Date", yaxis_title="Normalized Price",
    hovermode="x unified", height=400, template="plotly_white",
)
st.plotly_chart(fig_norm, use_container_width=True)

# ── VOLUME ────────────────────────────────────────────────────────────────────
if show_volume:
    st.header("Trading Volume Analysis")
    fig_vol = go.Figure()
    for company, df in stock_data.items():
        fig_vol.add_trace(go.Bar(
            x=df.index, y=df["Volume"], name=company, opacity=0.7,
            hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>%{y:,.0f}<extra></extra>",
        ))
    fig_vol.update_layout(
        title="Trading Volume Comparison",
        xaxis_title="Date", yaxis_title="Volume",
        barmode="group", hovermode="x unified",
        height=400, template="plotly_white",
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# ── STATISTICAL SUMMARY ───────────────────────────────────────────────────────
st.header("Statistical Summary")
rows = []
for company, df in stock_data.items():
    close = df["Close"]
    rows.append({
        "Company":       company,
        "Current Price": f"${float(close.iloc[-1]):.2f}",
        "Average Price": f"${float(close.mean()):.2f}",
        "Std Dev":       f"${float(close.std()):.2f}",
        "Total Return":  f"{((float(close.iloc[-1]) / float(close.iloc[0])) - 1) * 100:.2f}%",
        "Volatility":    f"{float(close.std()) / float(close.mean()) * 100:.2f}%",
    })
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ── EXPORT ────────────────────────────────────────────────────────────────────
st.header("Export Data")
frames = [df.assign(Company=company).reset_index() for company, df in stock_data.items()]
if frames:
    export_df = pd.concat(frames, ignore_index=True)
    st.download_button(
        label="⬇️ Download Data as CSV",
        data=export_df.to_csv(index=False),
        file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"**Data Sources:** Stooq / Yahoo Finance &nbsp;|&nbsp; "
    f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n"
    "**Disclaimer:** This tool is for educational purposes only. Not financial advice."
)
