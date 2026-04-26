import streamlit as st
import pandas as pd
import importlib
import training.config as config

# Reload config
importlib.reload(config)

from core.model import load_model, predict_pd
from core.scoring import calculate_scores, get_risk_level
from core.decision import get_decision
from core.business import calculate_lgd
from core.explain import get_feature_importance
from inference.user_data import load_user_data
from inference.inference_data_validation import validate_input_data
from inference.risk_category import GradeSubgrade

# -------------------------------
# Helper Functions
# -------------------------------

def get_thresholds():
    st.subheader("⚙️ Threshold Settings")

    low = st.slider("Lower Threshold", 0, 45, 30) / 100
    high = st.slider("Higher Threshold", 45, 100, 60) / 100
    recovery_rate = st.slider("Recovery Rate", 0, 100, 40) / 100
    ccf = st.slider("Credit Conversion Factor (CCF)", 0, 100, 75) / 100

    if low >= high:
        st.error("⚠️ Lower threshold must be less than higher threshold")
        st.stop()

    return round(low, 2), round(high, 2), round(recovery_rate, 2), round(ccf, 2)


def compute_ead(balance, limit, ccf):
    return balance + (limit - balance) * ccf


def compute_expected_loss(pd, lgd, ead):
    return pd * lgd * ead


def display_summary(prob, credit_score, original_score, grade):
    col1, col2, col3 = st.columns(3)

    col1.metric("PD", f"{prob:.2%}")

    delta = credit_score - original_score
    col2.metric("Credit Score", credit_score, delta)

    col3.metric("Grade", grade)


def display_risk_decision(prob, low, high, decision):
    if prob <= low:
        st.success(decision)
    elif prob <= high:
        st.warning(decision)
    else:
        st.error(decision)


def display_risk_metrics(pd, lgd, ead, el):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("PD", f"{pd*100:.2f}%")
    col2.metric("LGD", f"{lgd*100:.2f}%")
    col3.metric("EAD", f"₹{round(ead)}")
    col4.metric("Expected Loss", f"₹{round(el)}")


def display_explainability(model):
    features_df = get_feature_importance(model)

    with st.expander("🔍 Key Drivers"):
        st.caption("Feature importance shows relative contribution (not causation).")
        st.table(features_df.head())

        st.bar_chart(features_df.head().set_index("Cleaned_Features"))

        top_features = features_df['Cleaned_Features'].head(3).tolist()
        st.info(f"{', '.join(top_features)} are the top influencing features.")


# -------------------------------
# Main App
# -------------------------------

def RiskAssessment():
    st.title("🏦 Loan Default Risk Decision System")

    # Load model
    model = load_model()

    # Load & validate input
    user_inputs = load_user_data()
    df = pd.DataFrame([user_inputs])
    valid_df = validate_input_data(df)

    if valid_df.empty:
        st.error("⚠️ Invalid input data")
        st.stop()

    # Thresholds
    low, high, recovery_rate, ccf = get_thresholds()

    loan_amount = valid_df['LoanAmount'].iloc[0]
    if loan_amount <= 0:
        st.error("⚠️ Loan amount must be greater than 0")
        st.stop()

    # Predict
    if st.button("Predict"):

        # --- Prediction ---
        prob = predict_pd(model, valid_df)

        # --- Scores ---
        risk_score, credit_score = calculate_scores(prob)
        grade = GradeSubgrade(credit_score)
        risk_level = get_risk_level(grade)

        # --- Decision ---
        decision = get_decision(prob, low, high)

        # --- LGD & EAD ---
        lgd = 1 - recovery_rate

        balance = valid_df['CurrentBalance'].iloc[0]
        limit = valid_df['TotalCreditLimit'].iloc[0]
        ead = compute_ead(balance, limit, ccf)

        el = compute_expected_loss(prob, lgd, ead)

        # --- UI ---
        st.subheader("📊 Summary")
        display_summary(prob, credit_score, valid_df["CreditScore"].iloc[0], grade)

        display_risk_decision(prob, low, high, decision)

        st.metric("Risk Level", risk_level)

        st.info("""
        Decision Logic:
        • PD < Lower Threshold → Approve  
        • PD between thresholds → Review  
        • PD > Higher Threshold → Reject
        """)

        display_risk_metrics(prob, lgd, ead, el)

        display_explainability(model)
