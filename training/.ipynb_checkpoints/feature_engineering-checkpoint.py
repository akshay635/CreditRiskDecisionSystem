import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def make_ColumnTransformer(X_train):

    num_features = X_train.select_dtypes(exclude='object').columns.tolist()
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

    return preprocessor