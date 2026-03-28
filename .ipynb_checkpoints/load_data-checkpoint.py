import pandas as pd
import config

def load_data():
    df = pd.read_csv(config.DATA_PATH)
    df['loan_paid_back'] = 1 - df['loan_paid_back']
    df = df.replace(columns={'loan_paid_back':'loan_default'})
    return df