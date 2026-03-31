import importlib
import training.config as config
importlib.reload(config)
from pandera import Column, DataFrameSchema, Check

def validate_data(new_df):
    
#new_df = new_df[config.EXPECTED_FEATURES]
#assert new_df.columns.tolist() == config.EXPECTED_FEATURES
    try:
        schema = DataFrameSchema({
            'Age' : Column(int, checks=Check.in_range(18, 100), nullable=False),
            'Gender' : Column(str, checks=Check.isin(['Male', 'Female', 'Other']), nullable=False),
            'MaritalStatus': Column(str, checks=Check.isin(['Single', 'Married', 'Widowed', 'Divorced']), nullable=False),
            'EducationLevel': Column(str, checks=Check.isin(["Bachelor's", 'High school', "Master's", 'Other', 'Phd']), nullable=False),
            'AnnualIncome': Column(float, checks=Check.ge(0.0), nullable=False),
            'MonthlyIncome': Column(float, checks=Check.ge(0.0), nullable=False),
            'EmploymentStatus': Column(str, checks=Check.isin(["Employed", 'Self-employed', "Unemployed", 'Retired', 'Student']), nullable=False),
            'DebtToIncomeRatio': Column(float, checks=Check.in_range(0.0, 1.0), nullable=False),
            'LoanAmount': Column(float, checks=Check.ge(0.0), nullable=False),  
            'CreditScore': Column(int, checks=Check.in_range(300, 900), nullable=False),
            'LoanPurpose': Column(str, checks=Check.isin(['Debt consolidation', 'Other', 'Car',
                                                           'Home', 'Education', 'Business', 'Medical', 'Vacation']), nullable=False),
            'InterestRate': Column(float, checks=Check.in_range(1.0, 25.0), nullable=False),
            'LoanTerm': Column(int, checks= Check.in_range(12, 60), nullable=False),
            'Installment': Column(float, checks=Check.ge(0.0), nullable=False),
            'NumOfOpenAccounts': Column(int, nullable=False),
            'TotalCreditLimit': Column(float, checks=Check.ge(0.0), nullable=False),
            'CurrentBalance': Column(float, checks=Check.ge(0.0), nullable=False),
            'PublicRecords': Column(int, nullable=False), 
            'NumOfDelinquencies': Column(int, nullable=False),
            'LoanIncomeRatio': Column(float, nullable=False),
            'InstallmentIncomeRatio': Column(float, nullable=False),
            'CreditUtilization': Column(float, nullable=False)
            }, 
            
            checks=[
            # Row-wise check: no NaN in any row
            Check(lambda df: df.isna().sum() == 0, element_wise=False),
    
            # DataFrame-level check: no duplicate rows
            Check(lambda df: df.duplicated().sum() == 0, element_wise=False),
            
            # Total credit limit should always be higher than or equal to current outstanding balance
            Check(lambda df: df['TotalCreditLimit'] >= df['CurrentBalance'], element_wise=False)
        ])
    
        return schema.validate(new_df)
        
    except SchemaValidationError:
        # Code to handle the specific exception
        st.error("Error: Data/Schema mismatch error")
