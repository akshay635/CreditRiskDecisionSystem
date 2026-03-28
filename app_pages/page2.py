import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import importlib
import training.config as config

# Reload config (keep for safety)
importlib.reload(config)

from training.load_data import load_data

def PortfolioDashboard():

    # -------------------------------
    # Page Config
    # -------------------------------
    st.set_page_config(
        page_title="Credit Risk BI Dashboard",
        layout="wide"
    )

    st.markdown("# 🏦 Credit Risk BI Dashboard")
    st.markdown("### Real-time Loan Risk Monitoring & Decision System")
    st.markdown("---")

    # -------------------------------
    # Load Data
    # -------------------------------
    df = load_data()

    # -------------------------------
    # KPI Calculations
    # -------------------------------
    default_rate = df['LoanDefault'].mean() * 100
    med_annual_income = df['AnnualIncome'].median()
    med_monthly_income = df['MonthlyIncome'].median()
    avg_loan_amount = df['LoanAmount'].mean()

    max_credit_score = df['CreditScore'].max()
    min_credit_score = df['CreditScore'].min()
    avg_dti = df['DebtToIncomeRatio'].mean() * 100
    max_accounts = df['NumOfOpenAccounts'].max()
    avg_delinquencies = df['NumOfDelinquencies'].mean()

    # -------------------------------
    # Bucketing
    # -------------------------------
    df['DTIBucket'] = pd.qcut(
        df['DebtToIncomeRatio'], q=3, labels=['Low', 'Medium', 'High']
    )

    df['CreditScoreBucket'] = pd.qcut(
        df['CreditScore'], q=3, labels=['Low', 'Medium', 'High']
    )

    # -------------------------------
    # KPI Display
    # -------------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Loan Default Rate', f'{round(default_rate)}%')
    col2.metric('Median Annual Salary', f'₹{round(med_annual_income)}/-')
    col3.metric('Median Monthly Salary', f'₹{round(med_monthly_income)}/-')
    col4.metric('Avg Loan Exposure', f'₹{round(avg_loan_amount)}/-')

    col5, col6, col7, col8, col9 = st.columns(5)

    col5.metric('Max Credit Score', max_credit_score)
    col6.metric('Min Credit Score', min_credit_score)
    col7.metric('Avg Debt Burden', f'{round(avg_dti)}%')
    col8.metric('Max Credit Lines', max_accounts)
    col9.metric('Avg no of delinquencies', int(np.ceil(avg_delinquencies)))

    # -------------------------------
    # Aggregations
    # -------------------------------
    emp_default = df.groupby('EmploymentStatus')['LoanDefault'].mean().reset_index(name='DefaultRate')
    credit_default = df.groupby('CreditScoreBucket')['LoanDefault'].mean().reset_index(name='DefaultRate')
    dti_default = df.groupby('DTIBucket')['LoanDefault'].mean().reset_index(name='DefaultRate')

    st.markdown("---")

    # -------------------------------
    # Charts
    # -------------------------------
    col10, col11, col12 = st.columns(3)

    # Employment
    col10.subheader('Default rate by employment category')

    chart1 = alt.Chart(emp_default).mark_bar().encode(
        x='EmploymentStatus:N',
        y='DefaultRate:Q',
        color=alt.Color('DefaultRate:Q', scale=alt.Scale(scheme='redyellowgreen')),
        tooltip=['EmploymentStatus', 'DefaultRate']
    )

    col10.altair_chart(chart1, width=300, height=300)

    # Credit Score
    col11.subheader('Default rate by Credit Score bucket')

    chart2 = alt.Chart(credit_default).mark_bar().encode(
        x='CreditScoreBucket:N',
        y='DefaultRate:Q',
        color=alt.Color('DefaultRate:Q', scale=alt.Scale(scheme='redyellowblue')),
        tooltip=['CreditScoreBucket', 'DefaultRate']
    )

    col11.altair_chart(chart2, width=300, height=300)

    # DTI
    col12.subheader('Default rate by DTI Ratio bucket')

    chart3 = alt.Chart(dti_default).mark_bar().encode(
        x='DTIBucket:N',
        y='DefaultRate:Q',
        color=alt.Color('DefaultRate:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=['DTIBucket', 'DefaultRate']
    )

    col12.altair_chart(chart3, width=300, height=300)

    # -------------------------------
    # Insights
    # -------------------------------
    col13, col14, col15 = st.columns(3)

    emp_risk = emp_default.sort_values(by='DefaultRate', ascending=False).iloc[0]
    credit_risk = credit_default.sort_values(by='DefaultRate', ascending=False).iloc[0]
    dti_risk = dti_default.sort_values(by='DefaultRate', ascending=False).iloc[0]

    col13.info(
        f"📌 Highest risk segment: {emp_risk['EmploymentStatus']} "
        f"({emp_risk['DefaultRate']:.0%} default rate)",
        width=300
    )

    col14.info(
        f"📌 Highest risk segment: {credit_risk['CreditScoreBucket']} credit score bucket "
        f"({credit_risk['DefaultRate']:.0%} default rate)",
        width=300
    )

    col15.info(
        f"📌 Highest risk segment: {dti_risk['DTIBucket']} DTI bucket "
        f"({dti_risk['DefaultRate']:.0%} default rate)",
        width=300
    )

    st.markdown('---')

    # -------------------------------
    # Distribution Charts
    # -------------------------------
    col16, col17, col18 = st.columns(3)

    col16.subheader('Loan Default rate distribution of borrowers')
    fig = px.pie(df, names='LoanDefault')
    col16.plotly_chart(fig, width=300)
    col16.info("0: non-defaulters\n\n1: defaulters", width=300)

    col17.subheader('Distribution of Borrowers by Loan Purpose')
    fig1 = px.pie(df, names='LoanPurpose')
    col17.plotly_chart(fig1, width=400)

    col18.subheader('Employment status of borrowers')
    fig2 = px.pie(df, names='EmploymentStatus')
    col18.plotly_chart(fig2, width=400)
