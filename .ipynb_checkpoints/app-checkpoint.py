import streamlit as st
import pandas as pd
import numpy as np
import joblib
from training import config

st.set_page_config(page_title="Loan Default Risk Assessment", layout="centered")
st.title("🏦 Borrower credit worthiness check")

st.markdown(
    "This tool estimates the **risk of loan default** to support informed lending decisions."
)

final_model = joblib.load("models/final_ml_pipeline.joblib")

features = config.FEATURES

['loan_id', 'age', 'gender', 'marital_status', 'education_level', 'annual_income',
 'monthly_income', 'employment_status', 'debt_to_income_ratio','credit_score', 
 'loan_amount', 'loan_purpose', 'interest_rate', 'loan_term', 'installment', 
 'grade_subgrade', 'num_of_open_accounts','total_credit_limit', 'current_balance', 
 'delinquency_history', 'public_records', 'num_of_delinquencies', 'loan_default']

st.sidebar.header("👤 Borrower Details")
loan_id = st.sidebar.text_input('Enter the loan id')
name = st.sidebar.text_input('Enter the loan id')
age = st.sidebar.slider('Enter the age', 18, 100, 40)
annual_income = st.sidebar.slider('Enter the annual income', 0, 1_00_00_000, 1_00_000, 10_000)
monthly_income = round((annual_income/12), 2)
gender = st.sidebar.selectbox('Enter the gender', ['Male', 'Female', 'Other'])
marital_status = st.sidebar.selectbox('Enter the marital status', ['Single', 'Married', 'Widowed', 'Divorced']
education = st.sidebar.selectbox("Education Level", ["Bachelor's", "Master's", "High school", "Phd", "Other"])
employment = st.sidebar.selectbox("Employment Type", ["Employed", "Self-employed", "Unemployed", "Retired", "Student"])

st.sidebar.header("👤 Borrower Credit history details")
DTI = st.sidebar.slider('Debt To Income Ratio', 0.0, 1.0)
credit_score = st.sidebar.slider('Enter Credit Score', 300, 900)
num_of_open_accounts = st.sidebar.slider('Enter the number of open accounts', 0, 20)
total_credit_limit = st.sidebar.number_input('Enter the total available credit limit')
current_balance = st.sidebar.number_input('Enter the outstanding balance (loan + credit card)')
public_records = st.sidebar.selectbox('Negative public records (e.g., bankruptcies, legal actions)', options=[0, 1, 2])
num_of_delinquencies = st.sidebar.slider('Total delinquencies (missed payments)', 0, 12)

st.sidebar.header("👤 Borrower Loan details")
loan_amount = st.sidebar.number_input('Enter the annual income', 1_00_000)
interest_rate = st.sidebar.slider('Interest Rate(%)', 0.0, 25.0)
loan_term = st.sidebar.selectbox('Loan Term', [12, 24, 36, 48, 60])
loan_purpose = st.sidebar.selectbox("Purpose of the loan", ['Car', 'Debt consolidation', 'Business', 'Other', 
                                                            'Home', 'Medical', 'Education', 'Vacation'])
monthly_rate = (interest_rate/100)/12
installment = (loan_amount*monthly_rate*(1 + monthly_rate)**loan_term)/((1 + monthly_rate)**loan_term - 1)

user_inputs = {
    'age': age,
    'monthly_income': monthly_income,
    'gender': gender,
    'marital_status': marital_status,
    'education_level': education,
    'employment_status': employment,
    'debt_to_income_ratio': DTI,
    'credit_score': credit_score,
    'num_of_open_accounts': num_of_open_accounts,
    'total_credit_limit': total_credit_limit,
    'current_balance': current_balance,
    
}
