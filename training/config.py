# configuration files 

DATA_PATH = "data/loan_dataset_20000.csv"
MODEL_PATH = "models/final_ml_pipeline.joblib"

FEATURES = ['LoanID', 'Age', 'Gender', 'MaritalStatus', 'EducationLevel', 'AnnualIncome',
            'MonthlyIncome', 'EmploymentStatus', 'DebtToIncomeRatio','CreditScore', 
            'LoanAmount', 'LoanPurpose', 'InterestRate','LoanTerm', 'Installment', 
            'GradeSubgrade', 'NumOfOpenAccounts','TotalCreditLimit', 'CurrentBalance', 
            'DelinquencyHistory', 'PublicRecords', 'NumOfDelinquencies', 'LoanDefault']

HIGH_COLINEARITY = ['DelinquencyHistory', 'GradeSubgrade']

EXPECTED_FEATURES = ['Age', 'Gender', 'MaritalStatus', 'EducationLevel', 'AnnualIncome',
                     'MonthlyIncome', 'EmploymentStatus', 'DebtToIncomeRatio','CreditScore', 
                     'LoanAmount', 'LoanPurpose', 'InterestRate','LoanTerm', 'Installment', 
                     'NumOfOpenAccounts','TotalCreditLimit', 'CurrentBalance', 'PublicRecords', 
                     'NumOfDelinquencies']

LOWER_THRESHOLD = 0.30
HIGHER_THRESHOLD = 0.60

CONFUSION_MATRIX = 'artifacts/confusion_matrix.png'

CROSS_VALIDATION = 'artifacts/cv.csv'

METRICS = 'artifacts/metrics.csv'



