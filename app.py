import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import pickle
from pathlib import Path
from datetime import date
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="MedOptix | Hospital Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="auto"
)

# CUSTOM CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    
    /* Custom Header with Dashboard Color */
    .main-header {
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(90deg, #166362, #1f7a79);
        color: white;
        margin: -40px -40px 20px -40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 { color: white; margin: 0; font-weight: 700; font-size: 2.5rem; }
    .main-header p { color: #e0e0e0; font-size: 1.1rem; margin-top: 10px; }
    
    /* Metrics & Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #166362;
    }
    .risk-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .low-risk { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .medium-risk { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .high-risk { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        height: 3rem;
        background-color: #166362;
        color: white;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #124f4e; }
</style>
""", unsafe_allow_html=True)

# HELPER
def num_to_words(n):
    """Converts a number (0-999) to words for professional display."""
    if n == 0: return "Zero"
    
    under_20 = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    
    if n < 20:
        return under_20[n]
    if n < 100:
        return tens[n // 10] + ('' if n % 10 == 0 else '-' + under_20[n % 10].lower())
    if n < 1000:
        return under_20[n // 100] + ' Hundred' + ('' if n % 100 == 0 else ' ' + num_to_words(n % 100).lower())
    return str(n) # Fallback for larger numbers

# INTERNAL MODEL ENGINE 
@st.cache_resource
def load_resources():
    model_path = Path("model/sarimax_model.pkl")
    schema_path = Path("model/sarimax_schema.json")
    
    model = None
    schema = None
    error = None

    try:
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        else:
            return None, None, f"Model file not found at {model_path}."

        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = json.load(f)
        else:
            return None, None, f"Schema file not found at {schema_path}."
            
    except Exception as e:
        error = f"Error loading artifacts: {str(e)}"
    
    return model, schema, error

def run_internal_prediction(model, schema, steps, features):
    try:
        exog_df = pd.DataFrame([features] * steps)
        exog_df = exog_df.reindex(columns=schema, fill_value=0)
        forecast = model.forecast(steps=steps, exog=exog_df)
        predictions = [max(0, round(pred)) for pred in forecast.tolist()]
        return predictions, None
    except Exception as e:
        return [], str(e)


# 1. Header
st.markdown("""
    <div class="main-header">
        <h1>🩺 MedOptix Analytics</h1>
        <p>The HealSight Initiative: ML-Driven Hospital Capacity Planning</p>
    </div>
""", unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    st.image("image.png", width=60)
    st.title("Menu")
    st.info("System Status: ● Online")
    st.caption("v2.1.0 | © 2025 MedOptix")

# 3. Main Tabs
tab_dash, tab_tool, tab_context = st.tabs(["📊 Executive Dashboard", "🩺 ML Forecast Tool", "🧠 Model & Business Insights"])

# === TAB 1: POWER BI DASHBOARD ===
with tab_dash:
    st.markdown("### 🏥 Real-time Operations View")
    st.markdown("Live capacity, wait times, and operational bottlenecks across the network.")
    
    components.html(
        """
        <iframe 
            title="hospital_dashboad" 
            width="100%" 
            height="800" 
            src="https://app.powerbi.com/view?r=eyJrIjoiNDhlZjY4ZGQtNmM1ZC00NTg1LTg2NTktMDNhMDVmMDcwZGVmIiwidCI6IjhkMWE2OWVjLTAzYjUtNDM0NS1hZTIxLWRhZDExMmY1ZmI0ZiIsImMiOjN9&pageName=7d397389e9ded772290b" 
            frameborder="0" 
            allowFullScreen="true">
        </iframe>
        """,
        height=800,
        scrolling=True
    )

# === TAB 2: FORECAST TOOL ===
with tab_tool:
    MODEL, FEATURE_SCHEMA, LOAD_ERROR = load_resources()
    
    if LOAD_ERROR:
        st.error(f"🚨 System Error: {LOAD_ERROR}")
    else:
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.markdown("### 🔮 Generate Admissions Forecast")
            
            with st.form("prediction_form", border=True):
                # SECTION 1: SETTINGS
                st.markdown("#### 📅 Forecast Settings")
                s1, s2 = st.columns(2)
                with s1:
                    start_date = st.date_input("Forecast Start Date", value=date.today())
                with s2:
                    steps = st.slider("Forecast Horizon (Days)", 1, 30, 7)

                st.markdown("---")

                # SECTION 2: HOSPITAL CONTEXT
                c1, c2 = st.columns(2)
                with c1:
                    hospital = st.selectbox("Hospital", ["Helsinki Central Hospital", "Tampere City Hospital", "Turku University Hospital", "Oulu Regional Hospital"])
                with c2:
                    ward_code = st.selectbox("Ward Unit", ["ED", "ICU", "MED", "SURG"])

                # SECTION 3: OPERATIONAL INDICATORS
                st.markdown("#### Operational Indicators (Lagged Features)")
                r1, r2, r3 = st.columns(3)
                with r1: occupancy_rate = st.number_input("Occupancy Rate", 0.0, 1.0, 0.60, 0.01)
                with r2: overflow_lag = st.number_input("Overflow Patients", 0.0, 500.0, 42.0)
                with r3: avg_wait_lag = st.number_input("Avg Wait (Mins)", 0.0, 1000.0, 227.0)

                # SECTION 4: CAPACITY & STAFFING
                st.markdown("#### Capacity & Staffing")
                r4, r5, r6 = st.columns(3)
                with r4: base_beds = st.number_input("Base Beds", 1, 500, 30)
                with r5: eff_capacity = st.number_input("Effective Cap", 1, 500, 34)
                with r6: staffing = st.number_input("Staffing Index", 0.0, 2.0, 0.927)

                st.markdown("---")
                submitted = st.form_submit_button("🚀 Run Forecast")

        with col_side:
            st.markdown("### ℹ️ Guide")
            st.info("""
            **How to use:**
            1. Set your **Start Date** and **Horizon**.
            2. Select the Hospital and Ward.
            3. Input the **Lagged Features** (yesterday's data).
            4. Adjust **Capacity** to test scenarios.
            5. Click Run to predict demand.
            """)

        if submitted:
            payload = {
                "hospital": hospital, "ward": ward_code,
                "occupancy_rate_lag1": occupancy_rate, "overflow_lag1": overflow_lag,
                "avg_wait_minutes_lag1": avg_wait_lag, "base_beds": base_beds,
                "effective_capacity": eff_capacity, "staffing_index": staffing
            }
            
            with st.spinner("Running SARIMAX inference..."):
                forecast_vals, err = run_internal_prediction(MODEL, FEATURE_SCHEMA, steps, payload)
                
                if not err and forecast_vals:
                    st.success("Forecast generated successfully!")
                    
                    dates = pd.date_range(start=start_date, periods=len(forecast_vals))
                    df = pd.DataFrame({"Date": dates, "Admissions": forecast_vals})
                    
                    # 1. Result Display
                    if len(forecast_vals) == 1:
                        val = int(forecast_vals[0])
                        val_words = num_to_words(val)
                        
                        st.markdown(f"""
                        <div style="background-color:#f0f2f6; padding:30px; border-radius:10px; text-align:center;">
                            <h1 style="color:#166362; font-size:64px; margin:0;">{val}</h1>
                            <p style="font-size:24px; color:#555; margin-bottom:5px;"><strong>{val_words} Admissions</strong></p>
                            <p style="color:#888;">Predicted for {dates[0].strftime('%A, %b %d, %Y')}</p>
                            <p style="color:#166362; font-weight:bold; margin-top:10px;">{hospital} - {ward_code}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"### 📈 {steps}-Day Forecast Overview")
                        fig = px.line(df, x="Date", y="Admissions", markers=True)
                        fig.update_traces(line_color='#166362', line_width=3)
                        fig.update_layout(height=400, plot_bgcolor="white", hovermode="x unified")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        total_adm = int(sum(forecast_vals))
                        # UPDATED BOLD TEXT WITH HOSPITAL & WARD
                        st.markdown(f"**Total Predicted Inflow: {total_adm} ({num_to_words(total_adm)}) patients over {steps} days for {hospital} - {ward_code}.**")
                    
                    # 2. Risk Assessment
                    avg_vol = sum(forecast_vals) / len(forecast_vals)
                    if avg_vol < 5:
                        st.markdown('<div class="risk-card low-risk">🟢 Low Capacity Risk</div>', unsafe_allow_html=True)
                    elif avg_vol < 15:
                        st.markdown('<div class="risk-card medium-risk">🟡 Moderate Capacity Risk</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="risk-card high-risk">🔴 High Capacity Risk</div>', unsafe_allow_html=True)
                        
                else:
                    st.error(f"Prediction failed: {err}")

# === TAB 3: BUSINESS CONTEXT & MODEL ===
with tab_context:
    st.markdown("## 🧠 The HealSight Initiative")
    
    col_biz, col_model = st.columns(2)
    
    with col_biz:
        st.subheader("📋 Business Case")
        st.markdown("""
        **The Challenge: Reactive Operations**
        Hospitals in the Nordic public health network struggled with reactive capacity management, leading to:
        * ❌ **25% longer** patient waiting times.
        * ❌ **20% inefficiency** in bed allocation.
        * ❌ High staff burnout and overtime costs.

        **The Solution: MedOptix Analytics**
        A predictive capacity management suite designed to forecast patient inflows 7-30 days in advance, allowing administrators to align staffing and beds proactively.
        """)
        
        st.markdown("### 🏆 Quantifiable Impact")
        st.markdown("""
        <div class="metric-card">
            <h3>✅ 88%</h3>
            <p><strong>Bed Utilization Efficiency</strong><br>(Increased from 68%)</p>
        </div>
        <div style="margin-top:10px;"></div>
        <div class="metric-card">
            <h3>💰 €35,000 / mo</h3>
            <p><strong>Reduction in Overtime Costs</strong><br>(Down from €125k to €90k)</p>
        </div>
        """, unsafe_allow_html=True)

    with col_model:
        st.subheader("⚙️ Model Architecture")
        st.markdown("""
        **Algorithm:** SARIMAX (Seasonal Auto-Regressive Integrated Moving Average with eXogenous factors)
        
        **Why this model?**
        Unlike standard ARIMA, SARIMAX accounts for:
        1.  **Seasonality:** Weekly patterns in hospital admissions (e.g., higher on Mondays).
        2.  **External Drivers:** Uses operational data like *Wait Times* and *Staffing Index* to improve accuracy.
        """)
        
        st.markdown("### 📉 Performance Metrics")
        st.table(pd.DataFrame({
            "Metric": ["RMSE (Root Mean Sq Error)", "MAE (Mean Abs Error)", "R² (Accuracy)"],
            "Value": ["0.553", "0.463", "88.4%"],
            "Context": ["±0.5 patients error margin", "Very high precision", "Excellent fit"]
        }).set_index("Metric"))
        
        st.info("""
        **Feature Importance:**
        The model identifies **Occupancy Rate (Lag 1)** and **Overflow Count** as the strongest predictors of next-day demand.
        """)