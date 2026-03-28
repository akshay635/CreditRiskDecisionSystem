import pandas as pd
import numpy as np
import pandera as pa
from pandera import Column, DataFrameSchema, Check
import config

def valid_data(df):
    df['loan_id'] = 10000000 + df.index
    
    new_df = df[FEATURES]
    
    high_colinearity = HIGH_COLINEARITY
    
    new_df = new_df.drop(columns=high_colinearity)
    
    cat_cols = new_df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        new_df[col] = new_df[col].str.capitalize()

    schema = DataFrameSchema({
    'age' : Column(int, checks=Check.in_range(18, 100), nullable=False),
    'gender' : Column(str, checks=Check.isin(['Male', 'Female', 'Other']), nullable=False),
    'marital_status': Column(str, checks=Check.isin(['Single', 'Married', 'Widowed', 'Divorced']), nullable=False),
    'education_level': Column(str, checks=Check.isin(["Bachelor's", 'High school', "Master's", 'Other', 'Phd']), nullable=False),
    'monthly_income' : Column(float, checks=Check.ge(0.0), nullable=False),
    'employment_status': Column(str, checks=Check.isin(["Employed", 'Self-employed', "Unemployed", 'Retired', 'Student']), nullable=False),
    'debt_to_income_ratio': Column(float, checks=Check.in_range(0.0, 1.0), nullable=False),
    'loan_amount': Column(float, checks=Check.ge(0.0), nullable=False),  
    'credit_score': Column(int, checks=Check.in_range(300, 900), nullable=False),
    'loan_purpose': Column(str, checks=Check.isin(['Debt consolidation', 'Other', 'Car',
                                                   'Home', 'Education', 'Business', 'Medical', 'Vacation']), nullable=False),
    'interest_rate': Column(float, checks=Check.in_range(0.0, 25.0), nullable=False),
    'loan_term': Column(int, checks= Check.in_range(12, 60), nullable=False),
    'installment': Column(float, checks=Check.ge(0.0), nullable=False),
    'num_of_open_accounts': Column(int, nullable=False),
    'total_credit_limit': Column(float, checks=Check.ge(0.0), nullable=False),
    'current_balance': Column(float, checks=Check.ge(0.0), nullable=False),
    'public_records': Column(int, nullable=False), 
    'num_of_delinquencies': Column(int, nullable=False),
    'loan_default': Column(int, checks=Check.isin([0, 1]), nullable=False)
    })

    return schema.validate(new_df)
    


        