"""
Interactive Stock Market Analysis Tool
A Streamlit-based application for analyzing and comparing tech company stock performance.
Author: ACC102 Student
Date: April 2026
"""
import requests
import os

for key in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(key, None)


try:
    r = requests.get('https://httpbin.org/ip', timeout=10)
    print("your ip is :", r.json()['origin'])
except Exception as e:
    print("agent test fails:", e)

import time
import random
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Stock Market Analysis Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Interactive Stock Market Analysis Tool")
st.markdown("""
This tool provides real-time analysis of major tech company stocks, including price trends,
technical indicators, and comparative performance metrics.
""")

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.header("Configuration")

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Meta": "META",
    "Intel": "INTC"
}

selected_companies = st.sidebar.multiselect(
    "Select companies to analyze:",
    options=list(companies.keys()),
    default=["Apple", "Microsoft", "Tesla"]
)

date_range = st.sidebar.selectbox(
    "Select time period:",
    options=["1 Month", "3 Months", "6 Months", "1 Year", "2 Years"],
    index=2
)

date_mapping = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365, "2 Years": 730}
days      = date_mapping[date_range]
end_date  = datetime.now()
start_date = end_date - timedelta(days=days)

st.sidebar.header("Technical Indicators")
show_ma20   = st.sidebar.checkbox("Show 20-day Moving Average", value=True)
show_ma50   = st.sidebar.checkbox("Show 50-day Moving Average", value=True)
show_volume = st.sidebar.checkbox("Show Trading Volume",        value=True)

# ============================================================================
# DATA FETCHING  —  uses Ticker.history() + retry + back-off
# ============================================================================

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker: str, start: datetime, end: datetime):
    """Fetch OHLCV data with up to 3 retries and random back-off."""
    for attempt in range(3):
        try:
            data = yf.Ticker(ticker).history(
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d"),
                auto_adjust=True,
            )
            if data is None or data.empty:
                time.sleep(2 ** attempt + random.uniform(0, 1))
                continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in data.columns]
            data = data[keep].dropna(subset=["Close"])
            return data if not data.empty else None

        except Exception as e:
            msg = str(e)
            if "RateLimit" in msg or "Too Many Requests" in msg:
                wait = 5 * (attempt + 1) + random.uniform(1, 3)
                st.warning(f"⏳ {ticker}: 请求被限速，{wait:.0f} 秒后重试（{attempt+1}/3）...")
                time.sleep(wait)
            else:
                st.error(f"❌ 获取 {ticker} 数据失败：{e}")
                return None

    st.error(f"❌ {ticker}：3 次重试后仍失败，请稍后再试或更换网络。")
    return None


# ============================================================================
# HELPERS
# ============================================================================

def get_close(data: pd.DataFrame) -> pd.Series:
    s = data["Close"]
    return (s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s).squeeze()

def get_volume(data: pd.DataFrame) -> pd.Series:
    s = data["Volume"]
    return (s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s).squeeze()

@st.cache_data
def calculate_metrics(data: pd.DataFrame):
    if data is None or len(data) == 0:
        return None
    close = get_close(data)
    cur, prev = float(close.iloc[-1]), float(close.iloc[0])
    chg = cur - prev
    return {
        "current_price":    cur,
        "price_change":     chg,
        "price_change_pct": chg / prev * 100,
        "high_52w":         float(close.max()),
        "low_52w":          float(close.min()),
        "avg_volume":       float(get_volume(data).mean()),
    }

def add_moving_averages(data: pd.DataFrame) -> pd.DataFrame:
    close = get_close(data)
    data["MA20"] = close.rolling(20).mean()
    data["MA50"] = close.rolling(50).mean()
    return data

# ============================================================================
# MAIN
# ============================================================================

if selected_companies:
    stock_data, metrics_data = {}, {}

    with st.spinner("正在获取股票数据，请稍候..."):
        for company in selected_companies:
            ticker = companies[company]
            data = fetch_stock_data(ticker, start_date, end_date)
            if data is not None:
                data = add_moving_averages(data)
                stock_data[company]   = data
                metrics_data[company] = calculate_metrics(data)
            time.sleep(random.uniform(0.5, 1.5))   # gentle pacing

    # --- KEY METRICS ---
    st.header("Key Metrics")
    cols = st.columns(len(selected_companies))
    for idx, company in enumerate(selected_companies):
        m = metrics_data.get(company)
        if m:
            with cols[idx]:
                st.subheader(company)
                st.metric("Current Price",
                          f"${m['current_price']:.2f}",
                          f"{m['price_change']:.2f} ({m['price_change_pct']:.2f}%)")
                c1, c2 = st.columns(2)
                c1.metric("52W High", f"${m['high_52w']:.2f}")
                c2.metric("52W Low",  f"${m['low_52w']:.2f}")

    # --- PRICE TREND ---
    st.header("Price Trend Analysis")
    fig_price = go.Figure()
    for company in selected_companies:
        if company not in stock_data:
            continue
        data, close = stock_data[company], get_close(stock_data[company])
        fig_price.add_trace(go.Scatter(x=data.index, y=close, mode="lines", name=company,
            hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>"))
        if show_ma20 and "MA20" in data.columns:
            fig_price.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode="lines",
                name=f"{company} MA20", line=dict(dash="dash", width=1), opacity=0.5,
                hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>MA20: $%{y:.2f}<extra></extra>"))
        if show_ma50 and "MA50" in data.columns:
            fig_price.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode="lines",
                name=f"{company} MA50", line=dict(dash="dot", width=1), opacity=0.5,
                hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>MA50: $%{y:.2f}<extra></extra>"))
    fig_price.update_layout(title=f"Stock Price Trends ({date_range})", xaxis_title="Date",
        yaxis_title="Price (USD)", hovermode="x unified", height=500, template="plotly_white")
    st.plotly_chart(fig_price, use_container_width=True)

    # --- NORMALISED ---
    st.header("Performance Comparison")
    fig_norm = go.Figure()
    for company in selected_companies:
        if company not in stock_data:
            continue
        close = get_close(stock_data[company])
        norm  = close / float(close.iloc[0]) * 100
        fig_norm.add_trace(go.Scatter(x=norm.index, y=norm, mode="lines", name=company,
            hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>%{y:.2f}<extra></extra>"))
    fig_norm.update_layout(title="Normalized Price Performance (Base = 100)",
        xaxis_title="Date", yaxis_title="Normalized Price",
        hovermode="x unified", height=400, template="plotly_white")
    st.plotly_chart(fig_norm, use_container_width=True)

    # --- VOLUME ---
    if show_volume:
        st.header("Trading Volume Analysis")
        fig_vol = go.Figure()
        for company in selected_companies:
            if company not in stock_data:
                continue
            data = stock_data[company]
            fig_vol.add_trace(go.Bar(x=data.index, y=get_volume(data), name=company, opacity=0.7,
                hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>%{y:,.0f}<extra></extra>"))
        fig_vol.update_layout(title="Trading Volume Comparison", xaxis_title="Date",
            yaxis_title="Volume", barmode="group", hovermode="x unified",
            height=400, template="plotly_white")
        st.plotly_chart(fig_vol, use_container_width=True)

    # --- STATS ---
    st.header("Statistical Summary")
    rows = []
    for company in selected_companies:
        if company not in stock_data:
            continue
        close = get_close(stock_data[company])
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

    # --- EXPORT ---
    st.header("Export Data")
    frames = []
    for company in selected_companies:
        if company in stock_data:
            df = stock_data[company].copy()
            df["Company"] = company
            frames.append(df.reset_index())
    if frames:
        export_df = pd.concat(frames, ignore_index=True)
        st.download_button(
            label="⬇️ Download Data as CSV",
            data=export_df.to_csv(index=False),
            file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 Please select at least one company from the sidebar to begin analysis.")

st.markdown("---")
st.markdown(
    f"**Data Source:** Yahoo Finance API &nbsp;|&nbsp; "
    f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n"
    "**Disclaimer:** This tool is for educational purposes only. Not financial advice."
)
