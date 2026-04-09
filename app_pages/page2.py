
import streamlit as st
import pandas as pd
import numpy as np
import importlib
import training.config as config
importlib.reload(config)
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def BatchwisePrediction():
  st.title("Batchwise Portfolio Risk Analysis")

  uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

  if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.DataFrame(df)

  else:
    st.error('Invalid file, data not found. Please reupload it')
