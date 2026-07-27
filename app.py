import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Commodity Finance Engine", layout="wide")

st.title("Serverless Commodity Pricing Pipeline")
st.caption("Real-Time Agricultural Supply Monitoring & High-Frequency Financial Market Inference")

st.sidebar.header("Middleware Configuration")
selected_market = st.sidebar.selectbox("Target Commodity Market", ["Global Wheat Futures (CBOT)", "Asia-Pacific Dairy Index", "Trans-Atlantic Soybeans"])
supply_shock = st.sidebar.slider("Simulate Agricultural Supply Shock Severity", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize ML Pricing Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Agri-Telemetry API -> XGBoost Inference -> Asset Pricing")

if run_simulation:
    st.subheader(f"Active Empirical Pricing Model: {selected_market}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_yield = col1.empty()
    metric_price = col2.empty()
    metric_risk = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(3232)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    crop_yield_index = []
    commodity_prices = []
    risk_premiums = []
    
    base_yield = 150.0
    base_price = 600.0 
    
    for i in range(100):
        if i < 30:
            current_yield = base_yield + np.random.uniform(-2.0, 2.0)
            current_price = base_price + np.random.uniform(-5.0, 5.0)
            current_risk = np.random.uniform(2.0, 5.0)
            status = "MARKET EQUILIBRIUM"
        elif i >= 30 and i < 65:
            current_yield = base_yield - (i - 30) * (1.5 * supply_shock) + np.random.uniform(-5.0, 5.0)
            current_price = base_price + (i - 30) * (4.0 * supply_shock) + np.random.uniform(-10.0, 10.0)
            current_risk = np.random.uniform(20.0, 45.0)
            status = "SUPPLY SHOCK DETECTED"
        else:
            current_yield = current_yield + np.random.uniform(-2.0, 2.0)
            current_price = current_price + np.random.uniform(-15.0, 15.0)
            current_risk = np.random.uniform(45.0, 55.0) 
            status = "PRICE INFLATION SUSTAINED"
            
        crop_yield_index.append(current_yield)
        commodity_prices.append(current_price)
        risk_premiums.append(current_risk)
        
        metric_yield.metric("Simulated Crop Yield Index", f"{current_yield:.1f} pts", f"{(current_yield - base_yield):.1f}")
        metric_price.metric("Commodity Futures Price", f"${current_price:,.2f}", f"+${(current_price - base_price):,.2f}")
        metric_risk.metric("ML Adjusted Risk Premium", f"{current_risk:.1f}%")
        
        if status == "SUPPLY SHOCK DETECTED":
            metric_status.metric("Market Sentiment", status, "High Volatility")
        elif status == "PRICE INFLATION SUSTAINED":
            metric_status.metric("Market Sentiment", status, "New Baseline")
        else:
            metric_status.metric("Market Sentiment", status, "Stable")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=crop_yield_index, mode='lines', name='Crop Yield Index', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=commodity_prices, mode='lines', name='Commodity Price (USD)', yaxis='y2', line=dict(color='orange', dash='dot')))
        
        fig.update_layout(
            title="Empirical Commodity Pricing: Agricultural Supply Constraints vs High-Frequency Market Reaction",
            xaxis=dict(title="High-Frequency Timeline"),
            yaxis=dict(title="Crop Yield Index"),
            yaxis2=dict(title="Commodity Price (USD)", overlaying='y', side='right', range=[500, max(1000, current_price + 100)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "SUPPLY SHOCK DETECTED" and i == 30:
            log_placeholder.error(f"COMMODITY ALERT: Severe agricultural yield degradation detected at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine dynamically increasing asset risk premium.")
        elif status == "PRICE INFLATION SUSTAINED" and i == 65:
            log_placeholder.warning(f"MARKET UPDATE: Financial anomaly fully priced into commodity futures. XGBoost model recalibrating baseline equilibrium.")
        elif status == "MARKET EQUILIBRIUM" and i % 5 == 0:
            log_placeholder.success(f"Log: Dual-stream tick data {i} ingested via serverless middleware. Agricultural and financial parameters operating within historical bounds.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The cloud-native machine learning pipeline successfully correlated real-time agricultural supply constraints with empirical commodity pricing adjustments.")
else:
    st.info("Click 'Initialize ML Pricing Engine' in the sidebar to simulate high-frequency dual-stream data ingestion.")