import importlib
import training.config as config
importlib.reload(config)
from pandera import Column, DataFrameSchema, Check
from pandera.errors import SchemaValidationError

def validate_input_data(new_df):

    schema = DataFrameSchema(
        {
            'Age': Column(int, Check.in_range(18, 100), nullable=False),
            'Gender': Column(str, Check.isin(['Male', 'Female', 'Other']), nullable=False),
            'MaritalStatus': Column(str, Check.isin(['Single', 'Married', 'Widowed', 'Divorced']), nullable=False),
            'EducationLevel': Column(str, Check.isin(["Bachelor's", 'High school', "Master's", 'Other', 'Phd']), nullable=False),
            'AnnualIncome': Column(float, Check.ge(0.0), nullable=False),
            'MonthlyIncome': Column(float, Check.ge(0.0), nullable=False),
            'EmploymentStatus': Column(str, Check.isin(["Employed", 'Self-employed', "Unemployed", 'Retired', 'Student']), nullable=False),
            'DebtToIncomeRatio': Column(float, Check.in_range(0.0, 1.0), nullable=False),
            'LoanAmount': Column(float, Check.ge(0.0), nullable=False),
            'CreditScore': Column(int, Check.in_range(300, 900), nullable=False),
            'LoanPurpose': Column(str, Check.isin([
                'Debt consolidation', 'Other', 'Car', 'Home',
                'Education', 'Business', 'Medical', 'Vacation'
            ]), nullable=False),
            'InterestRate': Column(float, Check.in_range(1.0, 25.0), nullable=False),
            'LoanTerm': Column(int, Check.in_range(12, 60), nullable=False),
            'Installment': Column(float, Check.ge(0.0), nullable=False),
            'NumOfOpenAccounts': Column(int, nullable=False),
            'TotalCreditLimit': Column(float, Check.ge(0.0), nullable=False),
            'CurrentBalance': Column(float, Check.ge(0.0), nullable=False),
            'PublicRecords': Column(int, nullable=False),
            'NumOfDelinquencies': Column(int, nullable=False),
            'LoanIncomeRatio': Column(float, nullable=False),
            'InstallmentIncomeRatio': Column(float, nullable=False),
            'CreditUtilization': Column(float, nullable=False)
        },

        checks=[
            # No missing values
            Check(lambda df: df.isna().sum().sum() == 0),

            # No duplicate rows
            Check(lambda df: df.duplicated().sum() == 0),

            # Credit limit >= current balance
            Check(lambda df: (df['TotalCreditLimit'] >= df['CurrentBalance']).all())
        ]
    )

    try:
        validated_df = schema.validate(new_df)
        return validated_df

    except SchemaValidationError as e:
        st.error("⚠️ Data validation failed. Please check input values.")
        return None
