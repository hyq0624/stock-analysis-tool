"""
Interactive Stock Market Analysis Tool
A Streamlit-based application for analyzing and comparing tech company stock performance.
Author: ACC102 Student
Date: April 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
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

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📈 Interactive Stock Market Analysis Tool")
st.markdown("""
This tool provides real-time analysis of major tech company stocks, including price trends, 
technical indicators, and comparative performance metrics.
""")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.sidebar.header("Configuration")

# Company selection
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

# Date range selection
date_range = st.sidebar.selectbox(
    "Select time period:",
    options=["1 Month", "3 Months", "6 Months", "1 Year", "2 Years"],
    index=2
)

# Map date range to days
date_mapping = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
    "2 Years": 730
}

days = date_mapping[date_range]
end_date = datetime.now()
start_date = end_date - timedelta(days=days)

# Technical indicators
st.sidebar.header("Technical Indicators")
show_ma20 = st.sidebar.checkbox("Show 20-day Moving Average", value=True)
show_ma50 = st.sidebar.checkbox("Show 50-day Moving Average", value=True)
show_volume = st.sidebar.checkbox("Show Trading Volume", value=True)

# ============================================================================
# DATA FETCHING AND PROCESSING
# ============================================================================

@st.cache_data
def fetch_stock_data(ticker, start, end):
    """Fetch stock data from Yahoo Finance."""
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

@st.cache_data
def calculate_metrics(data):
    """Calculate key financial metrics."""
    if data is None or len(data) == 0:
        return None
    
    current_price = data['Close'].iloc[-1]
    previous_price = data['Close'].iloc[0]
    price_change = current_price - previous_price
    price_change_pct = (price_change / previous_price) * 100
    
    high_52w = data['Close'].max()
    low_52w = data['Close'].min()
    avg_volume = data['Volume'].mean()
    
    return {
        'current_price': current_price,
        'price_change': price_change,
        'price_change_pct': price_change_pct,
        'high_52w': high_52w,
        'low_52w': low_52w,
        'avg_volume': avg_volume
    }

def add_moving_averages(data):
    """Add moving average indicators to data."""
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    return data

# ============================================================================
# MAIN ANALYSIS SECTION
# ============================================================================

if selected_companies:
    # Fetch data for all selected companies
    stock_data = {}
    metrics_data = {}
    
    with st.spinner("Fetching stock data..."):
        for company in selected_companies:
            ticker = companies[company]
            data = fetch_stock_data(ticker, start_date, end_date)
            if data is not None:
                data = add_moving_averages(data)
                stock_data[company] = data
                metrics_data[company] = calculate_metrics(data)
    
    # Display metrics in columns
    st.header("Key Metrics")
    cols = st.columns(len(selected_companies))
    
    for idx, company in enumerate(selected_companies):
        if company in metrics_data:
            metrics = metrics_data[company]
            with cols[idx]:
                st.subheader(company)
                st.metric(
                    "Current Price",
                    f"${metrics['current_price']:.2f}",
                    f"{metrics['price_change']:.2f} ({metrics['price_change_pct']:.2f}%)"
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("52W High", f"${metrics['high_52w']:.2f}")
                with col2:
                    st.metric("52W Low", f"${metrics['low_52w']:.2f}")
    
    # ========================================================================
    # PRICE TREND CHART
    # ========================================================================
    
    st.header("Price Trend Analysis")
    
    fig_price = go.Figure()
    
    for company in selected_companies:
        if company in stock_data:
            data = stock_data[company]
            fig_price.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name=company,
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>'
            ))
            
            # Add moving averages
            if show_ma20:
                fig_price.add_trace(go.Scatter(
                    x=data.index,
                    y=data['MA20'],
                    mode='lines',
                    name=f'{company} MA20',
                    line=dict(dash='dash', width=1),
                    opacity=0.5,
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>MA20: $%{y:.2f}<extra></extra>'
                ))
            
            if show_ma50:
                fig_price.add_trace(go.Scatter(
                    x=data.index,
                    y=data['MA50'],
                    mode='lines',
                    name=f'{company} MA50',
                    line=dict(dash='dot', width=1),
                    opacity=0.5,
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>MA50: $%{y:.2f}<extra></extra>'
                ))
    
    fig_price.update_layout(
        title=f"Stock Price Trends ({date_range})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    # ========================================================================
    # PERFORMANCE COMPARISON
    # ========================================================================
    
    st.header("Performance Comparison")
    
    # Normalize prices to 100 at start date for comparison
    normalized_data = {}
    for company in selected_companies:
        if company in stock_data:
            data = stock_data[company]
            first_price = data['Close'].iloc[0]
            normalized_data[company] = (data['Close'] / first_price * 100)
    
    fig_normalized = go.Figure()
    for company in selected_companies:
        if company in normalized_data:
            fig_normalized.add_trace(go.Scatter(
                x=normalized_data[company].index,
                y=normalized_data[company],
                mode='lines',
                name=company,
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Normalized: %{y:.2f}<extra></extra>'
            ))
    
    fig_normalized.update_layout(
        title="Normalized Price Performance (Base = 100)",
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_normalized, use_container_width=True)
    
    # ========================================================================
    # TRADING VOLUME ANALYSIS
    # ========================================================================
    
    if show_volume:
        st.header("Trading Volume Analysis")
        
        fig_volume = go.Figure()
        
        for company in selected_companies:
            if company in stock_data:
                data = stock_data[company]
                fig_volume.add_trace(go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name=company,
                    opacity=0.7,
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Volume: %{y:,.0f}<extra></extra>'
                ))
        
        fig_volume.update_layout(
            title="Trading Volume Comparison",
            xaxis_title="Date",
            yaxis_title="Volume",
            barmode='group',
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # ========================================================================
    # STATISTICAL SUMMARY
    # ========================================================================
    
    st.header("Statistical Summary")
    
    summary_data = []
    for company in selected_companies:
        if company in stock_data:
            data = stock_data[company]
            summary_data.append({
                'Company': company,
                'Current Price': f"${data['Close'].iloc[-1]:.2f}",
                'Average Price': f"${data['Close'].mean():.2f}",
                'Std Dev': f"${data['Close'].std():.2f}",
                'Daily Return (%)': f"{((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100:.2f}%",
                'Volatility (%)': f"{(data['Close'].std() / data['Close'].mean() * 100):.2f}%"
            })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # ========================================================================
    # DATA EXPORT
    # ========================================================================
    
    st.header("Export Data")
    
    # Combine all data for export
    export_data = pd.DataFrame()
    for company in selected_companies:
        if company in stock_data:
            data = stock_data[company].copy()
            data['Company'] = company
            export_data = pd.concat([export_data, data.reset_index()])
    
    if not export_data.empty:
        csv = export_data.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 Please select at least one company from the sidebar to begin analysis.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
**Data Source:** Yahoo Finance API  
**Last Updated:** """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """  
**Disclaimer:** This tool is for educational purposes only. Not financial advice.
""")
