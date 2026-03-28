import pandas as pd
import importlib
import training.config as config
importlib.reload(config)

def load_data():
    df = pd.read_csv(config.DATA_PATH)
    df['loan_paid_back'] = 1 - df['loan_paid_back']
    df = df.rename(columns={'loan_paid_back':'LoanDefault'})
    df = df.rename(columns={
       'age': 'Age', 
       'gender': 'Gender', 
       'marital_status': 'MaritalStatus', 
       'education_level': 'EducationLevel',
       'annual_income': 'AnnualIncome',
       'monthly_income': 'MonthlyIncome',
       'employment_status': 'EmploymentStatus', 
       'debt_to_income_ratio': 'DebtToIncomeRatio', 
       'credit_score': 'CreditScore',
       'loan_amount': 'LoanAmount', 
       'loan_purpose': 'LoanPurpose', 
       'interest_rate': 'InterestRate', 
       'loan_term': 'LoanTerm',
       'installment': 'Installment', 
       'grade_subgrade': 'GradeSubgrade', 
       'num_of_open_accounts': 'NumOfOpenAccounts',
       'total_credit_limit':'TotalCreditLimit', 
       'current_balance': 'CurrentBalance', 
       'delinquency_history': 'DelinquencyHistory',
       'public_records': 'PublicRecords',
       'num_of_delinquencies': 'NumOfDelinquencies'})
    
    return df