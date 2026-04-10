# Importing required libraries
import streamlit as st
import pandas as pd
import numpy as np
import importlib
import training.config as config
importlib.reload(config)
from inference.inference_data_validation import validate_input_data
from core.model import load_model, predict_pd_batch
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def BatchwisePrediction():
  st.title("Batchwise Default Risk Analysis")

  uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

  if uploaded_file is not None:
    st.success('Data has been uploaded successfully')
  else:
    st.info('Please upload the file to proceed')
    st.stop()

  df = pd.read_csv(uploaded_file)

  # Function to convert to PascalCase
  def to_pascal_case(s):
      return ''.join(word.capitalize() for word in s.replace('_', ' ').split())
  
  # Apply to all column names
  df.columns = [to_pascal_case(col) for col in df.columns]

  df['LoanDefault'] = 1 - df['LoanPaidBack']

  target = 'LoanDefault'

  new_df = df.drop(columns=[target, 'LoanPaidBack'])
  new_df = new_df[config.EXPECTED_FEATURES]

  new_df['LoanIncomeRatio'] = round((new_df['LoanAmount'] / new_df['AnnualIncome']), 2)
  new_df['InstallmentIncomeRatio'] = round((new_df['Installment'] / new_df['MonthlyIncome']), 2)
  new_df['CreditUtilization'] = round((new_df['CurrentBalance'] / new_df['TotalCreditLimit']), 2)

  cat_cols = new_df.select_dtypes(include='object').columns.tolist()
  for col in cat_cols:
    new_df[col] = new_df[col].str.capitalize()

  #st.dataframe(new_df)
  actual = df[[target]]

  threshold = st.slider('Threshold value', 0.1, 0.9, 0.05)

  if st.button('Predict'):
    st.markdown("---")
    ml_model = load_model()
  
    probabilities = predict_pd_batch(ml_model, new_df)
  
    roc_auc = roc_auc_score(actual, probabilities)
    pr_auc = average_precision_score(actual, probabilities)

    st.container()
    col1, col2 = st.columns(2)
    col1.metric("ROC-AUC Score", round(roc_auc, 2), border=True)
    col2.metric("PR-AUC Score", round(pr_auc, 2), border=True)
    st.markdown("---")

    st.container()
    col3, col4, col5, col6 = st.columns(4)
    predictions = (probabilities >= threshold).astype(int)
    Accuracy = accuracy_score(actual, predictions)
    Precision = precision_score(actual, predictions)
    Recall = recall_score(actual, predictions)
    F1 = f1_score(actual, predictions)

    col3.metric("Accuracy", f"{round(Accuracy*100, 2)}%", border=True)
    col4.metric("Precision", f"{round(Precision*100, 2)}%", border=True)
    col5.metric("Recall", f"{round(Recall*100, 2)}%", border=True)
    col6.metric("F1", f"{round(F1*100, 2)}%", border=True)
    
    tn, fp, fn, tp = confusion_matrix(actual, predictions).ravel()

    flagged_risk = predictions.mean()

    st.markdown('---')
    st.container()
    col7, col8, col9, col10, col11 = st.columns(5)
    col7.metric('True Negatives', tn, border=True)
    col8.metric('False Negatives', fn, border=True)
    col9.metric('False Positives', fp, border=True)
    col10.metric('True Positives', tp, border=True)
    col11.metric('flagged_risk', round(flagged_risk*100, 2), border=True)

    st.markdown('---')

    new_df['LoanDefault'] = actual
    avg_loan_amount_d = new_df[new_df['LoanDefault'] == 1]['LoanAmount'].mean()
    avg_loan_amount_nd = new_df[new_df['LoanDefault'] == 0]['LoanAmount'].mean()
    avg_interest = (new_df['InterestRate'].mean())/100

    fp_cost = avg_loan_amount_nd * avg_interest
    fn_cost = avg_loan_amount_d + (avg_loan_amount_d*avg_interest)
    
    st.error('Expected_loss', f'{round(fp_cost + fn_cost)}/-')
    
