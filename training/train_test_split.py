from sklearn.model_selection import train_test_split

def Train_Test_Split(df):
    X = df.drop(columns=['LoanID', 'LoanDefault'])
    y = df[['LoanDefault']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3)

    return X_train, X_test, y_train, y_test