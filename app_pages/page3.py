import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import importlib
import training.config as config

importlib.reload(config)

from training.load_data import load_data


# -------------------------------
# Helper Functions
# -------------------------------

def compute_kpis(df):
    return {
        "default_rate": df['LoanDefault'].mean(),
        "med_annual_income": df['AnnualIncome'].median(),
        "med_monthly_income": df['MonthlyIncome'].median(),
        "avg_loan": df['LoanAmount'].mean(),
        "max_score": df['CreditScore'].max(),
        "min_score": df['CreditScore'].min(),
        "avg_dti": df['DebtToIncomeRatio'].mean(),
        "max_accounts": df['NumOfOpenAccounts'].max(),
        "avg_delinquencies": df['NumOfDelinquencies'].mean()
    }


def create_buckets(df):
    df = df.copy()

    df['DTIBucket'] = pd.qcut(df['DebtToIncomeRatio'], 3, labels=['Low', 'Medium', 'High'])
    df['CreditScoreBucket'] = pd.qcut(df['CreditScore'], 3, labels=['Low', 'Medium', 'High'])

    return df


def compute_segment_default(df):
    return {
        "employment": df.groupby('EmploymentStatus')['LoanDefault'].mean().reset_index(name='DefaultRate'),
        "credit": df.groupby('CreditScoreBucket')['LoanDefault'].mean().reset_index(name='DefaultRate'),
        "dti": df.groupby('DTIBucket')['LoanDefault'].mean().reset_index(name='DefaultRate')
    }


def plot_bar(data, x, y, color_scheme):
    return alt.Chart(data).mark_bar().encode(
        x=f"{x}:N",
        y=f"{y}:Q",
        color=alt.Color(f"{y}:Q", scale=alt.Scale(scheme=color_scheme)),
        tooltip=[x, y]
    )


def get_top_risk_segment(df, col):
    row = df.sort_values(by='DefaultRate', ascending=False).iloc[0]
    return row


# -------------------------------
# Main Dashboard
# -------------------------------

def PortfolioDashboard():

    st.set_page_config(page_title="Credit Risk BI Dashboard", layout="wide")

    st.title("🏦 Credit Risk BI Dashboard")
    st.caption("📊 Real-time Loan Risk Monitoring & Decision System")
    st.markdown("---")

    # -------------------------------
    # Load Data
    # -------------------------------
    df = load_data()

    # -------------------------------
    # KPI Section
    # -------------------------------
    kpi = compute_kpis(df)

    st.container()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Default Rate', f"{kpi['default_rate']*100:.1f}%")
    col2.metric('Median Annual Income', f"₹{kpi['med_annual_income']:.0f}")
    col3.metric('Median Monthly Income', f"₹{kpi['med_monthly_income']:.0f}")
    col4.metric('Avg Loan Amount', f"₹{kpi['avg_loan']:.0f}")

    col5, col6, col7, col8, col9 = st.columns(5)
    col5.metric('Max Credit Score', kpi['max_score'])
    col6.metric('Min Credit Score', kpi['min_score'])
    col7.metric('Avg DTI', f"{kpi['avg_dti']*100:.1f}%")
    col8.metric('Max Accounts', kpi['max_accounts'])
    col9.metric('Avg Delinquencies', int(np.ceil(kpi['avg_delinquencies'])))

    st.markdown("---")

    # -------------------------------
    # Bucketing & Aggregation
    # -------------------------------
    df = create_buckets(df)
    segments = compute_segment_default(df)

    # -------------------------------
    # Charts
    # -------------------------------
    col10, col11, col12 = st.columns(3)

    col10.subheader("Default by Employment")
    col10.altair_chart(plot_bar(segments["employment"], "EmploymentStatus", "DefaultRate", "redyellowgreen"))

    col11.subheader("Default by Credit Score")
    col11.altair_chart(plot_bar(segments["credit"], "CreditScoreBucket", "DefaultRate", "redyellowblue"))

    col12.subheader("Default by DTI")
    col12.altair_chart(plot_bar(segments["dti"], "DTIBucket", "DefaultRate", "viridis"))

    st.markdown("---")

    # -------------------------------
    # Insights
    # -------------------------------
    col13, col14, col15 = st.columns(3)

    emp = get_top_risk_segment(segments["employment"], 'EmploymentStatus')
    credit = get_top_risk_segment(segments["credit"], 'CreditScoreBucket')
    dti = get_top_risk_segment(segments["dti"], 'DTIBucket')

    col13.info(f"📌 Highest risk: {emp['EmploymentStatus']} ({emp['DefaultRate']:.0%})")
    col14.info(f"📌 Highest risk: {credit['CreditScoreBucket']} ({credit['DefaultRate']:.0%})")
    col15.info(f"📌 Highest risk: {dti['DTIBucket']} ({dti['DefaultRate']:.0%})")

    st.markdown("---")

    # -------------------------------
    # Distribution Charts
    # -------------------------------
    col16, col17, col18 = st.columns(3)

    # Default Distribution
    default_dist = df['LoanDefault'].value_counts(normalize=True) * 100

    fig = go.Figure(data=[go.Pie(
        labels=default_dist.index,
        values=default_dist.values,
        hole=0.4
    )])
    col16.subheader("Default Distribution")
    col16.plotly_chart(fig)

    # Loan Purpose
    fig2 = px.pie(df, names='LoanPurpose')
    col17.subheader("Loan Purpose Distribution")
    col17.plotly_chart(fig2)

    # Employment
    fig3 = px.pie(df, names='EmploymentStatus')
    col18.subheader("Employment Distribution")
    col18.plotly_chart(fig3)
