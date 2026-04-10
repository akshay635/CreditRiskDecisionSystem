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

  new_df['LoanIncomeRatio'] = round((df['LoanAmount'] / df['AnnualIncome']), 2)
  new_df['InstallmentIncomeRatio'] = round((df['Installment'] / df['MonthlyIncome']), 2)
  new_df['CreditUtilization'] = round((df['CurrentBalance'] / df['TotalCreditLimit']), 2)

  cat_cols = new_df.select_dtypes(include='object').columns.tolist()
  for col in cat_cols:
    new_df[col] = new_df[col].str.capitalize()

  st.dataframe(new_df)
  actual = df[['LoanDefault']]

  if st.button('Predict'):
    ml_model = load_model()
  
    probabilities = predict_pd_batch(ml_model, new_df)
  
    roc_auc = roc_auc_score(probabilities[0], actual.values)
    pr_auc = average_precision_score(probabilities[0], actual.values)
  
    col1, col2 = st.columns(2)
    col1.metric("ROC-AUC Score", round(roc_auc, 2))
    col2.metric("PR-AUC Score", round(pr_auc, 2))
