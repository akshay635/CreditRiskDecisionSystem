import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

def Cross_Validate(X_train, y_train, models, preprocessor):
    
    scoring = {
        'Accuracy': 'accuracy',
        'Precision' : 'precision',
        'Recall': 'recall',
        'F1': 'f1',
        'PR_AUC_score' : 'average_precision',
        'ROC_AUC_score': 'roc_auc'
    }
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = []
    
    for name, model in models.items():
        pipe = Pipeline(steps=[
            ('preprocessing', preprocessor),
            ('ml_model', model)
        ])
        cv_result = cross_validate(
            pipe,
            X_train,
            y_train.values.ravel(),
            cv=skf,
            scoring=scoring,
            n_jobs=-1,
        )
        row = {
            "model": name,
            "accuracy": cv_result["test_Accuracy"].mean(),
            "precision": cv_result["test_Precision"].mean(),
            "recall": cv_result["test_Recall"].mean(),
            "f1": cv_result["test_F1"].mean(),
            "pr_auc": cv_result["test_PR_AUC_score"].mean(),
            'roc_auc': cv_result['test_ROC_AUC_score'].mean()
        }
        results.append(row)

    cv_results = pd.DataFrame(results).sort_values(by='pr_auc', ascending=False)
    print(cv_results)

    best_ml_model = cv_results.iloc[0]['model']
    return best_ml_model, cv_results