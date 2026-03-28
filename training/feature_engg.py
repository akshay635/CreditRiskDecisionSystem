from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def make_ColumnTransformer(X_train, X_test):
    
    X_train['LoanIncomeRatio'] = round((X_train['LoanAmount'] / X_train['AnnualIncome']), 2)
    X_train['InstallmentIncomeRatio'] = round((X_train['Installment'] / X_train['MonthlyIncome']), 2)
    X_train['CreditUtilization'] = round((X_train['CurrentBalance'] / X_train['TotalCreditLimit']), 2)
    X_test['LoanIncomeRatio'] = round((X_test['LoanAmount'] / X_test['AnnualIncome']), 2)
    X_test['InstallmentIncomeRatio'] = round((X_test['Installment'] / X_test['MonthlyIncome']), 2)
    X_test['CreditUtilization'] = round((X_test['CurrentBalance'] / X_test['TotalCreditLimit']), 2)

    X_train = X_train.drop(columns=['AnnualIncome'])
    X_test = X_test.drop(columns=['AnnualIncome'])
    num_features = X_train.select_dtypes(exclude=['object', 'category']).columns.tolist()
    cat_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
            
    num_transformer = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder())
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_features),
        ('cat', cat_transformer, cat_features)
    ], remainder='passthrough')

    return preprocessor, X_train, X_test