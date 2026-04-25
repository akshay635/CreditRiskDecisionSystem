import pandas as pd
import streamlit as st
import importlib
import training.config as config

# Reload config (keep for safety)
importlib.reload(config)

from app_pages.page1 import RiskAssessment
from app_pages.page2 import BatchwisePrediction
from app_pages.page3 import PortfolioDashboard
from app_pages.page4 import CreditScoreCalculator
from app_pages.page5 import EMICalculator
from app_pages.page6 import ModelDashboard

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config("Credit Risk App", page_icon='🏦', layout='wide')

# -------------------------------
# Sidebar Navigation
# -------------------------------
page = st.sidebar.selectbox(
    "Select Page",
    [
        'Home',
        "Single Borrower Risk Estimation",
        'Batchwise Risk Estimation',
        "Portfolio Dashboard",
        "Credit Score Calculator",
        "EMI Calculator",
        "Model Performance metrics"
    ]
)

# -------------------------------
# Routing
# -------------------------------

if page == 'Home':
    st.title("🏦 Credit Risk Decision System for Loan Default Prediction and NPA Reduction")
    st.info("👈 Click the arrow on the left to open the sidebar")
    st.markdown('---')

    st.subheader("📌 Overview")
    st.info("This application predicts the probability of loan default and helps identify high-risk borrowers to reduce financial loss.")
    st.markdown('---')

    st.subheader("🔍 Problem Statement")
    st.info("""
    Banks and NBFCs face increasing NPAs due to ineffective identification of high-risk borrowers.
    """)
    st.markdown('---')
    
    st.subheader("💡 Solution")
    st.info("""
    - Predicts probability of default (PD)
    - Segments borrowers into risk categories (Low / Medium / High)
    - Supports single and batch predictions
    """)
    st.markdown('---')
    
    st.subheader("💰 Business Impact")
    st.info("""
    - Reduces credit loss by identifying high-risk borrowers
    - Controls opportunity cost from rejecting good borrowers
    - Enables data-driven lending decisions
    """)
    st.markdown('---')
    
    st.subheader("⚙️ How to Use")
    st.info("""
    1. Navigate to **Single Borrower Risk Estimation** for individual analysis  
    2. Use **Batchwise Risk Estimation** for portfolio-level insights  
    3. Monitor model performance in **Model Performance Metrics section**
    """)
    st.markdown('---')
    
elif page == "Single Borrower Risk Estimation":
    RiskAssessment()

elif page == "Batchwise Risk Estimation":
    BatchwisePrediction()

elif page == "Portfolio Dashboard":
    PortfolioDashboard()

elif page == "Credit Score Calculator":

    st.title("💳 Credit Score Calculator")

    payment_history = st.slider("Payment History (%)", 0, 100)
    cu_ratio = st.slider("Credit Utilization Ratio", 0.0, 1.0)
    history_years = st.number_input("Credit History (in years)", 0)
    credit_inquiries = st.number_input("No of credit inquiries", 0)

    calc = CreditScoreCalculator(
        payment_history, cu_ratio, history_years, credit_inquiries
    )

    score = calc.calculate_score()
    st.success(f"Credit Score: {score}")

    st.plotly_chart(calc.plot_gauge())


elif page == "EMI Calculator":

    st.title("💵 EMI Calculator")

    principal = st.number_input("Enter the principal amount")

    if principal < 1000:
        st.error("Please enter valid amount")

    rate = st.slider("Enter the Interest rate (%)", 1.0, 30.0)

    if rate < 1.0 or rate > 30.0:
        st.error("Please provide valid interest rate")

    tenure = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60])

    emi_calc = EMICalculator(principal, rate, tenure)
    emi = emi_calc.calculate()

    st.subheader(f"EMI: ₹{emi}/-")
    emi_calc.plot(emi)

else:
    ModelDashboard()
    
    
    
    
    
