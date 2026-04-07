import pandas as pd
import streamlit as st
import importlib
import training.config as config

# Reload config (keep for safety)
importlib.reload(config)

from app_pages.page1 import RiskAssessment
from app_pages.page2 import PortfolioDashboard
from app_pages.page3 import CreditScoreCalculator
from app_pages.page4 import EMICalculator
from app_pages.page5 import ModelDashboard

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config("Credit Risk Decision System", page_icon='🏦')

# -------------------------------
# Sidebar Navigation
# -------------------------------
page = st.sidebar.selectbox(
    "Select Page",
    [
        "Risk Assessment",
        "Portfolio Dashboard",
        "Credit Score Calculator",
        "EMI Calculator",
        "Model Performance metrics"
    ]
)

# -------------------------------
# Routing
# -------------------------------
if page == "Risk Assessment":
    RiskAssessment()

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
    
    
    
    
    
