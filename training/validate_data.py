import importlib
import training.config as config
importlib.reload(config)
from pandera import Column, DataFrameSchema, Check

def valid_data(df):
    df['LoanID'] = 10000000 + df.index
    new_df = df[['LoanID', 'Age', 'Gender', 'MaritalStatus', 'EducationLevel', 'AnnualIncome',
                 'MonthlyIncome', 'EmploymentStatus', 'DebtToIncomeRatio','CreditScore', 
                 'LoanAmount', 'LoanPurpose', 'InterestRate','LoanTerm', 'Installment', 
                 'NumOfOpenAccounts','TotalCreditLimit', 'CurrentBalance', 'DelinquencyHistory',
                 'PublicRecords', 'NumOfDelinquencies', 'GradeSubgrade', 'LoanDefault']]

    high_colinearity = config.HIGH_COLINEARITY

    new_df = new_df.drop(columns=high_colinearity)

    cat_cols = new_df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        new_df[col] = new_df[col].str.capitalize()

    schema = DataFrameSchema({
        'Age' : Column(int, checks=Check.in_range(18, 100), nullable=False),
        'Gender' : Column(str, checks=Check.isin(['Male', 'Female', 'Other']), nullable=False),
        'MaritalStatus': Column(str, checks=Check.isin(['Single', 'Married', 'Widowed', 'Divorced']), nullable=False),
        'EducationLevel': Column(str, checks=Check.isin(["Bachelor's", 'High school', "Master's", 'Other', 'Phd']), nullable=False),
        'AnnualIncome' : Column(float, checks=Check.ge(0.0), nullable=False),
        'MonthlyIncome' : Column(float, checks=Check.ge(0.0), nullable=False),
        'EmploymentStatus': Column(str, checks=Check.isin(["Employed", 'Self-employed', "Unemployed", 'Retired', 'Student']), nullable=False),
        'DebtToIncomeRatio': Column(float, checks=Check.in_range(0.0, 1.0), nullable=False),
        'LoanAmount': Column(float, checks=Check.ge(0.0), nullable=False),  
        'CreditScore': Column(int, checks=Check.in_range(300, 850), nullable=False),
        'LoanPurpose': Column(str, checks=Check.isin(['Debt consolidation', 'Other', 'Car', 'Home', 
                                                      'Education', 'Business', 'Medical', 'Vacation']), nullable=False),
        'InterestRate': Column(float, checks=Check.in_range(0.0, 25.0), nullable=False),
        'LoanTerm': Column(int, checks= Check.in_range(12, 60), nullable=False),
        'Installment': Column(float, checks=Check.ge(0.0), nullable=False),
        'NumOfOpenAccounts': Column(int, nullable=False),
        'TotalCreditLimit': Column(float, checks=Check.ge(0.0), nullable=False),
        'CurrentBalance': Column(float, checks=Check.ge(0.0), nullable=False),
        'PublicRecords': Column(int, nullable=False), 
        'NumOfDelinquencies': Column(int, nullable=False),
        'LoanDefault': Column(int, checks=Check.isin([0, 1]), nullable=False)}, 
        checks=[
        # Row-wise check: no NaN in any row
        Check(lambda df: df.isna().sum() == 0, element_wise=False),

        # DataFrame-level check: no duplicate rows
        Check(lambda df: df.duplicated().sum() == 0, element_wise=False),
        
        # Total credit limit should always be higher than or equal to current outstanding balance
        Check(lambda df: df['TotalCreditLimit'] >= df['CurrentBalance'], element_wise=False)
    ])

    return schema.validate(new_df)
    


        