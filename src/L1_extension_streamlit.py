"""
Level 1: Interactive Streamlit Dashboard

A web-based interactive portfolio calculator using Streamlit.
Fetches live data from Yahoo Finance and computes risk/return metrics in real-time.

Run with: streamlit run L1_extension_streamlit.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from src.L1_calculator import PortfolioCalculator


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Portfolio Calculator - Level 1",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR: DATA INPUT
# ============================================================================

st.sidebar.markdown("## 📈 Portfolio Configuration")
st.sidebar.markdown("---")

# Ticker Input
st.sidebar.subheader("1️⃣ Choose Assets")
default_tickers = "AAPL, MSFT, GOOGL, AMZN"
tickers_input = st.sidebar.text_input(
    "Enter tickers (comma-separated):",
    value=default_tickers,
    help="e.g., AAPL, MSFT, GOOGL"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
n_assets = len(tickers)

if n_assets == 0:
    st.error("❌ Please enter at least one ticker")
    st.stop()

# Date Range
st.sidebar.subheader("2️⃣ Historical Period")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime("2024-01-01"),
        help="Beginning of historical data"
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=pd.to_datetime("2025-01-01"),
        help="End of historical data"
    )

# Risk-Free Rate
st.sidebar.subheader("3️⃣ Risk Parameters")
rf_rate = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=3.0,
    step=0.1,
    help="Annual risk-free rate (e.g., 10-year Treasury)"
) / 100.0

# Portfolio Weights
st.sidebar.subheader("4️⃣ Asset Allocation Weights")
st.sidebar.caption(f"Adjust weights for {n_assets} asset{'s' if n_assets > 1 else ''}")

raw_weights = []
weight_cols = st.sidebar.columns(2)
for i, ticker in enumerate(tickers):
    col = weight_cols[i % 2]
    with col:
        val = st.number_input(
            f"{ticker} Weight",
            min_value=0.0,
            max_value=1.0,
            value=1.0 / n_assets,
            step=0.05,
            key=f"weight_{ticker}"
        )
        raw_weights.append(val)

# Normalize weights
weights_array = np.array(raw_weights)
total_weight = np.sum(weights_array)

if total_weight == 0:
    st.error("❌ Sum of weights cannot be zero")
    st.stop()

weights = weights_array / total_weight

# Display normalized weights in sidebar
st.sidebar.markdown("---")
st.sidebar.caption("📊 Normalized Allocations")
weight_df = pd.DataFrame({
    "Asset": tickers,
    "Weight": [f"{w:.2%}" for w in weights]
})
st.sidebar.dataframe(weight_df, use_container_width=True, hide_index=True)


# ============================================================================
# MAIN: DATA FETCHING & COMPUTATION
# ============================================================================

st.markdown("# 📊 Portfolio Risk & Return Calculator")
st.markdown("*Level 1: Interactive Dashboard*")
st.markdown("---")

# Status messages
with st.spinner("📥 Fetching historical data..."):
    try:
        # Download data
        pdata = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            progress=False,
            interval="1d"
        )
        
        # Handle single vs multiple ticker structure
        if n_assets == 1:
            df_close = pdata["Close"].to_frame(name=tickers[0])
        else:
            df_close = pdata["Close"]
        
        df_close = df_close.dropna()
        
        if df_close.empty:
            st.error("❌ No data found for the selected tickers and date range")
            st.stop()
        
        st.success(f"✅ Downloaded {len(df_close)} trading days")
        
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        st.stop()

# Compute statistics using PortfolioCalculator
with st.spinner("🔄 Computing portfolio metrics..."):
    try:
        calc = PortfolioCalculator(df_close, risk_free_rate=rf_rate)
        log_returns = calc.compute_log_returns()
        mu, sigma = calc.compute_statistics()
        
        # Portfolio metrics
        portfolio_return, portfolio_volatility, sharpe_ratio = calc.portfolio_metrics(weights)
        
        st.success("✅ Calculation complete")
        
    except Exception as e:
        st.error(f"❌ Calculation error: {str(e)}")
        st.stop()


# ============================================================================
# SECTION 1: KEY PORTFOLIO METRICS
# ============================================================================

st.markdown("## 📈 Portfolio Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Expected Return",
        f"{portfolio_return:.2%}",
        help="Annualized expected return based on historical mean"
    )

with col2:
    st.metric(
        "Annual Volatility",
        f"{portfolio_volatility:.2%}",
        help="Annualized standard deviation of returns"
    )

with col3:
    st.metric(
        "Sharpe Ratio",
        f"{sharpe_ratio:.4f}",
        help="Return per unit of risk (higher is better)"
    )

with col4:
    # Return/Risk ratio
    return_to_risk = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
    st.metric(
        "Return/Risk Ratio",
        f"{return_to_risk:.4f}",
        help="Expected return divided by volatility"
    )

st.markdown("---")


# ============================================================================
# SECTION 2: INDIVIDUAL ASSET STATISTICS
# ============================================================================

st.markdown("## 📊 Individual Asset Statistics")

asset_stats = pd.DataFrame({
    "Asset": tickers,
    "Expected Return": [f"{mu[i]:.2%}" for i in range(n_assets)],
    "Volatility": [f"{np.sqrt(sigma[i, i]):.2%}" for i in range(n_assets)],
    "Sharpe Ratio": [
        f"{(mu[i] - rf_rate) / np.sqrt(sigma[i, i]):.4f}" 
        for i in range(n_assets)
    ]
})

col1, col2 = st.columns([2, 1])
with col1:
    st.dataframe(asset_stats, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 📋 Summary")
    best_sharpe_idx = np.argmax([
        (mu[i] - rf_rate) / np.sqrt(sigma[i, i]) 
        for i in range(n_assets)
    ])
    st.markdown(f"**Best Sharpe**: {tickers[best_sharpe_idx]}")
    st.markdown(f"**Highest Return**: {tickers[np.argmax(mu)]}")
    st.markdown(f"**Lowest Risk**: {tickers[np.argmin(np.diag(sigma))]}")

st.markdown("---")


# ============================================================================
# SECTION 3: NORMALIZED PRICE PERFORMANCE
# ============================================================================

st.markdown("## 📈 Normalized Stock Performance")
st.caption("Base 100 = starting price. Shows relative growth across assets.")

normalized_prices = (df_close / df_close.iloc[0]) * 100

fig_prices = go.Figure()
for ticker in tickers:
    fig_prices.add_trace(go.Scatter(
        x=normalized_prices.index,
        y=normalized_prices[ticker],
        name=ticker,
        mode='lines',
        line=dict(width=2)
    ))

fig_prices.update_layout(
    title="Normalized Price Performance (Base = 100)",
    xaxis_title="Date",
    yaxis_title="Normalized Price",
    hovermode='x unified',
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig_prices, use_container_width=True)

st.markdown("---")


# ============================================================================
# SECTION 4: COVARIANCE & CORRELATION MATRICES
# ============================================================================

st.markdown("## 🔗 Covariance & Correlation Analysis")

col1, col2 = st.columns(2)

# Covariance Matrix
with col1:
    st.subheader("Covariance Matrix (Σ)")
    cov_df = pd.DataFrame(sigma, index=tickers, columns=tickers)
    st.dataframe(
        cov_df.style.format("{:.6f}"),
        use_container_width=True
    )

# Correlation Matrix
with col2:
    st.subheader("Correlation Matrix (ρ)")
    
    # Compute correlation from covariance
    diag_std = np.sqrt(np.diag(sigma))
    correlation = sigma / np.outer(diag_std, diag_std)
    corr_df = pd.DataFrame(correlation, index=tickers, columns=tickers)
    
    st.dataframe(
        corr_df.style.format("{:.4f}"),
        use_container_width=True
    )

st.markdown("---")

# ============================================================================
# SECTION 5: RETURNS DISTRIBUTION
# ============================================================================

st.markdown("## 📊 Log Returns Distribution")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Return Statistics")
    returns_stats = pd.DataFrame({
        "Asset": tickers,
        "Mean Daily Return": [f"{log_returns[ticker].mean():.4%}" for ticker in tickers],
        "Daily Volatility": [f"{log_returns[ticker].std():.4%}" for ticker in tickers],
        "Min Return": [f"{log_returns[ticker].min():.2%}" for ticker in tickers],
        "Max Return": [f"{log_returns[ticker].max():.2%}" for ticker in tickers],
    })
    st.dataframe(returns_stats, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Distribution Visualization")
    
    fig_dist = go.Figure()
    for ticker in tickers:
        fig_dist.add_trace(go.Histogram(
            x=log_returns[ticker] * 100,
            name=ticker,
            opacity=0.7,
            nbinsx=50
        ))
    
    fig_dist.update_layout(
        title="Daily Log Returns Distribution (%)",
        xaxis_title="Return (%)",
        yaxis_title="Frequency",
        barmode='overlay',
        height=400,
        template="plotly_white"
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 6: DATA DOWNLOAD & EXPORT
# ============================================================================

st.markdown("## 💾 Data Export")

col1, col2, col3 = st.columns(3)

with col1:
    # Download returns
    returns_csv = log_returns.to_csv(index=True)
    st.download_button(
        label="📥 Download Log Returns",
        data=returns_csv,
        file_name=f"log_returns_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

with col2:
    # Download prices
    prices_csv = df_close.to_csv(index=True)
    st.download_button(
        label="📥 Download Prices",
        data=prices_csv,
        file_name=f"prices_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

with col3:
    # Download summary
    summary_data = {
        "Metric": [
            "Portfolio Return",
            "Portfolio Volatility",
            "Sharpe Ratio",
            "Risk-Free Rate"
        ],
        "Value": [
            f"{portfolio_return:.4f}",
            f"{portfolio_volatility:.4f}",
            f"{sharpe_ratio:.4f}",
            f"{rf_rate:.4f}"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_csv = summary_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Summary",
        data=summary_csv,
        file_name=f"portfolio_summary_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

st.markdown("---")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
---
### 📖 About This Dashboard

**Level 1: Risk & Return Calculator** - Interactive portfolio analysis tool.

**Features:**
- 🔍 Real-time data from Yahoo Finance
- 📊 Multi-asset portfolio analysis
- 📈 Risk/return metrics (return, volatility, Sharpe)
- 💾 Data export capabilities

**Methodology:**
- Log returns for accuracy
- 252-day annualization
- Historical covariance estimation

**Disclaimer:** For educational purposes only. Not investment advice.

---
*Built with Streamlit | Portfolio Optimization*
""")
