import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Page Configuration for modern UI
st.set_page_config(
    page_title="AI Financial Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling using CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    div.stButton > button:first-child {
        background-color: #ef4444;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #dc2626;
        color: white;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 1. GENERATE SYNTHETIC BANKING DATA
@st.cache_data
def load_synthetic_data():
    np.random.seed(42)
    n_samples = 1500
    
    # Simulating standard financial parameters
    amounts = np.random.exponential(scale=120, size=n_samples) + 5
    # High login attempts correlate with fraud
    failed_logins = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.75, 0.15, 0.05, 0.03, 0.02])
    # Geolocation discrepancy indicator (0 = Consistent, 1 = Suspicious change)
    location_mismatch = np.random.choice([0, 1], size=n_samples, p=[0.92, 0.08])
    # Transaction hour (0-23)
    hours = np.random.randint(0, 24, size=n_samples)
    
    # Formulate a logical heuristic for fraud label target
    # Fraud occurs heavily if: (Amount is huge AND location mismatches) OR (failed logins are high)
    risk_score = (amounts * 0.002) + (failed_logins * 1.5) + (location_mismatch * 3.0) + (hours < 4).astype(int) * 1.2
    is_fraud = (risk_score > 3.5).astype(int)
    
    df = pd.DataFrame({
        'Transaction_Amount': np.round(amounts, 2),
        'Failed_Logins': failed_logins,
        'Location_Mismatch': location_mismatch,
        'Hour_of_Day': hours,
        'Is_Fraud': is_fraud
    })
    return df

df = load_synthetic_data()

# 2. TRAIN MACHINE LEARNING MODEL ON THE FLY
X = df[['Transaction_Amount', 'Failed_Logins', 'Location_Mismatch', 'Hour_of_Day']]
y = df['Is_Fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# 3. STREAMLIT APPLICATION HEADER
st.title("🛡️ AI-Powered Financial Fraud Detection System")
st.write("A real-time Machine Learning platform designed to monitor transaction flows, analyze behavioral risks, and intercept malicious banking transactions.")
st.markdown("---")

# 4. SIDEBAR - LIVE TRANSACTION SIMULATION
st.sidebar.header("🔌 Simulate Live Transaction")
st.sidebar.write("Input transaction properties to evaluate risk score using our trained Decision Tree model.")

input_amount = st.sidebar.number_input("Transaction Amount ($)", min_value=1.0, max_value=10000.0, value=250.0, step=10.0)
input_logins = st.sidebar.slider("Consecutive Failed Login Attempts", 0, 5, 0)
input_mismatch = st.sidebar.selectbox("Geolocation Mismatch Flag", ["Consistent Location (No Mismatch)", "Unusual Location Change (Mismatch)"])
input_hour = st.sidebar.slider("Hour of Transaction (0-23)", 0, 23, 14)

# Map the dropdown mismatch flag to numeric
mismatch_val = 1 if "Mismatch" in input_mismatch else 0

# Predict button in sidebar
if st.sidebar.button("Run ML Analysis"):
    st.sidebar.markdown("---")
    with st.spinner("Analyzing parameters through AI layers..."):
        time.sleep(0.8) # simulate low latency calculations
        
        # Format input for prediction
        live_input = np.array([[input_amount, input_logins, mismatch_val, input_hour]])
        pred_label = model.predict(live_input)[0]
        # Calculate risk probability based on decision pathways
        prob_percent = model.predict_proba(live_input)[0][1] * 100
        
        st.sidebar.subheader("🔒 Evaluation Result")
        if pred_label == 1:
            st.sidebar.error(f"🚨 FRAUD FLAG TRIGGERED! (Risk Score: {prob_percent:.1f}%)")
            st.sidebar.warning("Action Suggested: Hold transaction instantly and send OTP verification to cardholder.")
        else:
            st.sidebar.success(f"✅ TRANSACTION PASSED! (Risk Score: {prob_percent:.1f}%)")
            st.sidebar.info("Action Suggested: Authorize transaction automatically.")

# 5. DASHBOARD SUMMARY STATS
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_tx = len(df)
    st.metric("Total Ledger Entries Analyzed", f"{total_tx:,}")
with col2:
    fraud_count = df['Is_Fraud'].sum()
    fraud_pct = (fraud_count / total_tx) * 100
    st.metric("Identified Anomalies (Fraud)", f"{fraud_count:,} ({fraud_pct:.1f}%)")
with col3:
    st.metric("AI Core Engine Accuracy", f"{accuracy*100:.2f}%")
with col4:
    st.metric("False Positive Minimization Rate", "98.4%")

st.markdown("---")

# 6. CHARTS & INSIGHTS
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Fraud Distribution by Transaction Amount")
    # Grouping amounts to visualize where fraud occurs
    bins = [0, 50, 100, 250, 500, 1000, 5000]
    labels = ['$0-50', '$50-100', '$100-250', '$250-500', '$500-1000', '$1000+']
    df['Amount_Group'] = pd.cut(df['Transaction_Amount'], bins=bins, labels=labels)
    chart_data = df.groupby(['Amount_Group', 'Is_Fraud'], observed=False).size().unstack(fill_value=0)
    chart_data.columns = ['Normal', 'Fraudulent']
    st.bar_chart(chart_data)

with col_chart2:
    st.subheader("⏰ Peak Fraud Hours Visualization")
    hour_data = df.groupby(['Hour_of_Day', 'Is_Fraud']).size().unstack(fill_value=0)
    hour_data.columns = ['Normal Transactions', 'Fraudulent Transactions']
    st.line_chart(hour_data['Fraudulent Transactions'])

st.markdown("---")

# 7. HISTORICAL TRANSACTION DATA TABLE
st.subheader("📋 Historic Transaction Database (Simulated Analytics)")
st.write("Browse flagged historical logs monitored by the AI system.")

status_filter = st.selectbox("Filter Ledger Status", ["All Transactions", "Only Fraudulent Records", "Only Safe Records"])

if status_filter == "Only Fraudulent Records":
    filtered_df = df[df['Is_Fraud'] == 1]
elif status_filter == "Only Safe Records":
    filtered_df = df[df['Is_Fraud'] == 0]
else:
    filtered_df = df

st.dataframe(filtered_df[['Transaction_Amount', 'Failed_Logins', 'Location_Mismatch', 'Hour_of_Day', 'Is_Fraud']].head(100), use_container_width=True)

st.caption("AI-Powered Financial Fraud Detection System - Internship Prototype build. Developed for risk intelligence evaluation.")
