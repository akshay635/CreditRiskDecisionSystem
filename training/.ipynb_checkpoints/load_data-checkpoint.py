import pandas as pd
import src.config as config
importlib.reload(config)
from src.config import RiskConfig

def load_data():
    df = pd.read_csv('loan_dataset_20000.csv')
    df['loan_paid_back'] = 1 - df['loan_paid_back']
    df = df.replace(columns={'loan_paid_back':'loan_default'})
    return df