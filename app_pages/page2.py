
import streamlit as st
import pandas as pd
import numpy as np
import importlib
import training.config as config
importlib.reload(config)
from inference.inference_data_validation import validate_input_data
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def BatchwisePrediction():
  st.title("Batchwise Default Risk Analysis")

  uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.DataFrame(df)

  else:
    st.info('Please upload the file to proceed')

  df['LoanIncomeRatio'] = round((df['LoanAmount'] / df['AnnualIncome']), 2)
  df['InstallmentIncomeRatio'] = round((df['Installment'] / df['MonthlyIncome']), 2)
  df['CreditUtilization'] = round((df['CurrentBalance'] / df['TotalCreditLimit']), 2)

  valid_df = validate_input_data(df)

  if valid_df is not None:
    st.success('Data is valid')
  else:
    st.warning('Data is invalid')
    
