import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import optuna
import joblib
import mlflow
import mlflow.sklearn
import hashlib

from training.custom_transformer import SkewTransformer
from training.load_data import load_data
from training.validate_data import valid_data
from training.train_test_split import Train_Test_Split
from training.feature_engg import make_ColumnTransformer
from training.cross_validation import Cross_Validate

from optuna.samplers import TPESampler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# -------------------------------
# Load & Prepare Data
# -------------------------------
df = load_data()
valid_df = valid_data(df)

X_train, X_test, y_train, y_test = Train_Test_Split(valid_df)
preprocessor, X_train, X_test = make_ColumnTransformer(X_train, X_test)

# -------------------------------
# Handle Imbalance
# -------------------------------
pos = np.sum(y_train['LoanDefault'] == 0)
neg = np.sum(y_train['LoanDefault'] == 1)

scale_pos_weight = round(pos / neg)
print(scale_pos_weight)

# -------------------------------
# Models
# -------------------------------
models = {
    'Logistic Regression': LogisticRegression(class_weight={0:1, 1:scale_pos_weight}, random_state=42),
    'Decision Tree': DecisionTreeClassifier(class_weight={0:1, 1:scale_pos_weight}, random_state=42),
    'Random Forest': RandomForestClassifier(class_weight={0:1, 1:scale_pos_weight}, random_state=42),
    'XGBoost': XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42),
    'LightGBM': LGBMClassifier(class_weight={0:1, 1:scale_pos_weight}, random_state=42)
}

# -------------------------------
# Cross Validation
# -------------------------------
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
best_model, cv_results = Cross_Validate(X_train, y_train, models, preprocessor)

num_cols = X_train.select_dtypes(exclude='object').columns.tolist()

# -------------------------------
# Hyperparameter Tuning (Optuna)
# -------------------------------
def objective(trial):

    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 2, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1),
        'num_leaves': trial.suggest_int('num_leaves', 2, 32),
        'min_split_gains': trial.suggest_float('min_split_gains', 0.0, 1.0),
        'min_child_weight': trial.suggest_float('min_child_weight', 0.001, 0.1),
        'min_child_samples': trial.suggest_int('min_child_samples', 20, 60),
        'subsample': trial.suggest_float('subsample', 0.0, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.0, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 1.0),
        'class_weight': {0:1, 1:scale_pos_weight},
        'random_state': 42
    }

    lgbm_model = models[best_model]
    lgbm_model.set_params(**params)

    final_lgbm_pipe = Pipeline(steps=[
        ('skew', SkewTransformer(numeric_features=num_cols)),
        ('preprocessing', preprocessor),
        ('model', lgbm_model)
    ])

    cv_scores = cross_val_score(
        final_lgbm_pipe,
        X_train,
        y_train.values.ravel(),
        cv=skf,
        scoring='average_precision',
        n_jobs=-1
    )

    return cv_scores.mean()


study = optuna.create_study(
    sampler=TPESampler(),
    direction='maximize',
    study_name='LGBM_model',
    storage='sqlite:///db.sqlite'
)

study.optimize(objective, n_trials=50)

best_params = study.best_params
best_score = study.best_value

# -------------------------------
# Final Model
# -------------------------------
final_lgbm = LGBMClassifier(
    class_weight={0:1, 1:scale_pos_weight},
    random_state=42,
    **best_params
)

final_pipeline = Pipeline(steps=[
    ('skew', SkewTransformer(numeric_features=num_cols)),
    ('preprocessing', preprocessor),
    ('model', final_lgbm)
])

final_pipeline.fit(X_train, y_train.values.ravel())

# -------------------------------
# Evaluation
# -------------------------------
prob = final_pipeline.predict_proba(X_test)[:, 1]

roc_auc = roc_auc_score(y_test, prob)
pr_auc = average_precision_score(y_test, prob)

threshold = 0.45
pred = (prob >= threshold).astype(int)

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)

metrics_df = pd.DataFrame([{
    'model': best_model,
    'ROC-AUC': roc_auc,
    'PR-AUC': pr_auc,
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1': f1
}]).sort_values(by='PR-AUC', ascending=False)

metrics_df.to_csv("artifacts/metrics.csv", index=False)
cv_results.to_csv("artifacts/cv.csv", index=False)

# -------------------------------
# Logs
# -------------------------------
print("Model evaluation scores for best performing model")
print("Threshold:", threshold)
print("ROC-AUC:", roc_auc)
print("PR-AUC:", pr_auc)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))

# -------------------------------
# Save Model
# -------------------------------
joblib.dump(final_pipeline, "models/final_ml_pipeline.joblib")

# -------------------------------
# Confusion Matrix Plot
# -------------------------------
fig, ax = plt.subplots()
sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
ax.set_title("Confusion Matrix")

plt.tight_layout()
plt.savefig("artifacts/confusion_matrix.png")
plt.close()

# -------------------------------
# MLflow Logging
# -------------------------------
data_hash = hashlib.md5(
    open('data/loan_dataset_20000.csv', 'rb').read()
).hexdigest()

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Loan_Default_ML_model_LGBM")
mlflow.autolog(log_models=False)

with mlflow.start_run(run_name=best_model) as run:
    run_id = run.info.run_id

    mlflow.log_params(best_params)

    mlflow.log_metrics({
        "cv_mean_pr_auc": best_score,
        "test_accuracy": accuracy,
        "test_recall": recall,
        "test_precision": precision,
        "test_f1": f1,
        "test_roc_auc": roc_auc,
        "test_pr_auc": pr_auc
    })

    mlflow.sklearn.log_model(final_pipeline, "LGBM_Classifier")
    mlflow.log_artifact("artifacts/confusion_matrix.png")

    mlflow.log_params({
        "dataset_hash": data_hash,
        "decision_threshold": threshold
    })

model_uri = f"runs:/{run_id}/LGBM_Classifier"

mlflow.register_model(
    model_uri=model_uri,
    name="Loan_Default_Model_LGBM"
)

print("Logged to MLflow successfully.")
