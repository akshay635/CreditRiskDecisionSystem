import streamlit as st
import pandas as pd
import importlib
import training.config as config

# Reload config (keep as-is for safety)
importlib.reload(config)

from core.model import load_model, predict_pd
from core.scoring import calculate_scores, get_risk_level
from core.decision import get_decision
from core.business import calculate_lgd, expected_loss
from core.explain import get_feature_importance
from inference.user_data import load_user_data
from inference.inference_data_validation import validate_data
from inference.risk_category import GradeSubgrade


def RiskAssessment():
    st.title("🏦 Credit Risk Decision System")

    # -------------------------------
    # Load Model
    # -------------------------------
    model = load_model()

    # -------------------------------
    # User Input & Validation
    # -------------------------------
    user_inputs = load_user_data()
    df = pd.DataFrame([user_inputs])
    valid_df = validate_data(df)

    if valid_df.empty:
        st.error("⚠️ Invalid input data. Please check inputs.")
        st.stop()

    # -------------------------------
    # Threshold Settings
    # -------------------------------
    st.subheader("Setting up thresholds")

    low = st.slider("Lower Threshold", 0.0, 0.45, 0.30)
    high = st.slider("Higher Threshold", 0.45, 1.0, 0.60)

    if low >= high:
        st.error("Invalid threshold limits. ⚠️ Lower threshold must be less than higher threshold")
        st.stop()

    loan_amount = valid_df['LoanAmount'].iloc[0]

    if loan_amount <= 0:
        st.error("⚠️ Loan amount must be greater than 0")
        st.stop()
    # -------------------------------
    # Prediction Trigger
    # -------------------------------
    if st.button("Predict"):

        # ---- Prediction ----
        prob = predict_pd(model, valid_df)

        # ---- Scoring ----
        risk_score, credit_score = calculate_scores(prob)
        grade = GradeSubgrade(credit_score)
        risk_level = get_risk_level(grade)

        # ---- Decision ----
        decision = get_decision(prob, low, high)

        # ---- Business Metrics ----
        loan_purpose = valid_df["LoanPurpose"].iloc[0]
        loan_amount = valid_df["LoanAmount"].iloc[0]

        lgd = calculate_lgd(loan_purpose)
        loss = expected_loss(prob, loan_amount, lgd)

        # -------------------------------
        # UI: Summary
        # -------------------------------
        st.subheader("📊 Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Probability of Default (PD)", f"{prob:.2%}")

        delta = credit_score - valid_df["CreditScore"].iloc[0]
        col2.metric("Credit Score", credit_score, delta)

        col3.metric("Expected Loss", f"₹{round(loss)}/-")
        col4.metric("Grade", grade)

        st.metric("Decision", decision)
        st.metric("Risk Level", risk_level)

        st.caption("""
        Decision is based on Probability of Default (PD):
        • PD < Lower Threshold → Low Risk (Approve)
        • PD between thresholds → Medium Risk (Review)
        • PD > Higher Threshold → High Risk (Reject)
        """)

        # -------------------------------
        # Explainability
        # -------------------------------
        features_df = get_feature_importance(model)

        with st.expander("Key drivers of the outcome"):
            st.caption("Feature importance shows relative contribution to prediction (not causation).")
            st.table(features_df.head())

            st.bar_chart(
                features_df.head().set_index("Cleaned_Features")
            )

            top_1 = features_df['Cleaned_Features'].iloc[0]
            top_2 = features_df['Cleaned_Features'].iloc[1]
            top_3 = features_df['Cleaned_Features'].iloc[2]
            st.info(f"{top_1}, {top_2} and {top_3} are the key features which are influencing the final outcome.")
