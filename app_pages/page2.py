import streamlit as st
import pandas as pd
import numpy as np
import importlib
import training.config as config

importlib.reload(config)

from core.model import load_model, predict_pd_batch
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

# -------------------------------
# Helper Functions
# -------------------------------

def to_pascal_case(s):
    return ''.join(word.capitalize() for word in s.replace('_', ' ').split())


def preprocess_data(df):
    df.columns = [to_pascal_case(col) for col in df.columns]

    if set(df.columns) != set(config.BATCH_FEATURES):
        st.error("Invalid data. Features are missing.")
        st.stop()

    df['LoanDefault'] = 1 - df['LoanPaidBack']

    new_df = df.drop(columns=['LoanDefault', 'LoanPaidBack'])
    new_df = new_df[config.EXPECTED_FEATURES]

    # Feature Engineering
    new_df['LoanIncomeRatio'] = new_df['LoanAmount'] / new_df['AnnualIncome']
    new_df['InstallmentIncomeRatio'] = new_df['Installment'] / new_df['MonthlyIncome']
    new_df['CreditUtilization'] = new_df['CurrentBalance'] / new_df['TotalCreditLimit']

    # Clean categorical
    cat_cols = new_df.select_dtypes(include='object').columns
    for col in cat_cols:
        new_df[col] = new_df[col].str.capitalize()

    return new_df, df['LoanDefault']


def get_thresholds():
    threshold = st.slider('Threshold', 10, 90, 50) / 100
    ccf = st.slider("CCF", 0, 100, 75) / 100

    return threshold, ccf


def compute_metrics(actual, probs, threshold):
    preds = (probs >= threshold).astype(int)

    metrics = {
        "roc_auc": roc_auc_score(actual, probs),
        "pr_auc": average_precision_score(actual, probs),
        "accuracy": accuracy_score(actual, preds),
        "precision": precision_score(actual, preds),
        "recall": recall_score(actual, preds),
        "f1": f1_score(actual, preds),
        "conf_matrix": confusion_matrix(actual, preds),
        "preds": preds
    }

    return metrics


def compute_business_metrics(df, probs, preds, ccf):
    df = df.copy()

    df['Probabilities'] = probs
    df['Predictions'] = preds
    
    mappings = {
    'Home': 0.2,
    'Car': 0.35,
    'Educational': 0.3,
    'Medical': 0.35,
    'Debt consolidation': 0.45,
    'Vacation': 0.5,
    'Business': 0.5,
    'Others': 0.6
    }

    df['RR'] = df['LoanPurpose'].map(mappings)
    
    # LGD & EAD
    df['EAD'] = df['CurrentBalance'] + (df['TotalCreditLimit'] - df['CurrentBalance']) * ccf
    df['LGD'] = df['EAD']*(1 - df['RR'])

    df['ExpectedLoss'] = df['Probabilities'] * df['LGD'] * df['EAD']
    df['PDExposure'] = (df['Probabilities']*df['EAD'])
    weightedPD = df['PDExposure'].sum()/df['EAD'].sum()
    
    # Cost calculation
    avg_loan_d = df[df['LoanDefault'] == 1]['LoanAmount'].mean()
    avg_loan_nd = df[df['LoanDefault'] == 0]['LoanAmount'].mean()
    avg_interest = df['InterestRate'].mean() / 100

    fn_cost = avg_loan_d * (1 + avg_interest)
    fp_cost = avg_loan_nd * avg_interest

    tn, fp, fn, tp = confusion_matrix(df['LoanDefault'], preds).ravel()

    return {
        "df": df,
        "npas": fn * fn_cost,
        "opportunity_cost": fp * fp_cost,
        "weighted_pd": weightedPD,
        "avg_pd": df['Probabilities'].mean(),
        "avg_lgd": df['LGD'].mean(),
        "avg_ead": df['EAD'].mean(),
        "avg_el": df['ExpectedLoss'].mean(),
        "total_el": df['ExpectedLoss'].sum(),
        "conf": (tn, fp, fn, tp)
    }


# -------------------------------
# Main Function
# -------------------------------

def BatchwisePrediction():
    st.title("📊 Loan Default Risk - Batch Prediction")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file is None:
        st.info("Upload file to proceed")
        st.stop()

    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully")

    processed_df, actual = preprocess_data(df)

    threshold, ccf = get_thresholds()

    if st.button("Predict"):
        model = load_model()

        probs = predict_pd_batch(model, processed_df)

        metrics = compute_metrics(actual, probs, threshold)
        business = compute_business_metrics(
            df, probs, metrics["preds"], recovery_rate, ccf
        )

        # -------------------------------
        # Display Metrics
        # -------------------------------
        with st.container():
            col1, col2 = st.columns(2)
            col1.metric("ROC-AUC", round(metrics["roc_auc"], 2), border=True)
            col2.metric("PR-AUC", round(metrics["pr_auc"], 2), border=True)

        st.markdown("---")
        with st.container():
            col3, col4, col5, col6 = st.columns(4)
            col3.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%", border=True)
            col4.metric("Precision", f"{metrics['precision']*100:.2f}%", border=True)
            col5.metric("Recall", f"{metrics['recall']*100:.2f}%", border=True)
            col6.metric("F1", f"{metrics['f1']*100:.2f}%", border=True)

        tn, fp, fn, tp = business["conf"]

        st.markdown("---")
        with st.container():
            col7, col8, col9, col10 = st.columns(4)
            col7.metric("TN", tn, border=True)
            col8.metric("FN", fn, border=True)
            col9.metric("FP", fp, border=True)
            col10.metric("TP", tp, border=True)

        st.markdown("---")
        with st.container():
            col11, col12, col13 = st.columns(3)
            col11.metric("Opportunity Cost", round(business["opportunity_cost"]), border=True)
            col12.metric("NPAs", round(business["npas"]), border=True)
            col13.metric("Weighted PD", f"{business['weighted_pd']*100:.2f}%", border=True)

        st.markdown("---")
        with st.container():
            col14, col15, col16, col17 = st.columns(4)
            col14.metric("Avg PD", f"{business['avg_pd']*100:.2f}%", border=True)
            col15.metric("Avg LGD", f"{business['avg_lgd']*100:.2f}%", border=True)
            col16.metric("Avg EAD", round(business["avg_ead"]), border=True)
            col17.metric("Total EL", round(business["total_el"]), border=True)

        # -------------------------------
        # Risk Segmentation
        # -------------------------------
        df_result = business["df"]

        df_result["Risk Bucket"] = pd.cut(
            df_result['Probabilities'],
            bins=[0, 0.3, 0.6, 1],
            labels=["Low", "Medium", "High"]
        )

        st.bar_chart(df_result["Risk Bucket"].value_counts())

        # -------------------------------
        # Download
        # -------------------------------
        st.download_button(
            "Download Results",
            df_result.to_csv(index=False),
            "scored_portfolio.csv"
        )
