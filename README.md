# Credit Risk Decision System

🔹 Project Title

Credit Risk BI Dashboard & ML Decision System

🔹 Overview

This project is an end-to-end Credit Risk Analytics System that integrates Machine Learning and Business Intelligence dashboards to support loan decision-making.

It predicts borrower default risk and provides both individual-level decisions and portfolio-level insights.

🔹 Objectives
Predict Probability of Default (PD) for borrowers
Classify borrowers into risk segments
Support loan approval decisions
Analyze portfolio-level credit risk

🔹 Features

🔸 Risk Assessment Engine

Predicts Probability of Default (PD)
Dynamically updates credit score
Segments borrowers into risk categories
Generates decisions: Approve / Review / Reject

🔸 Credit Risk BI Dashboard

Portfolio KPIs (default rate, income, DTI, etc.)
Risk segmentation:
Employment status
Credit score buckets
DTI buckets
Automated insights highlighting high-risk segments
Borrower distribution analysis

🔸 Financial Tools

1)Credit score simulator
2)EMI calculator

🔸 Model Performance Dashboard

Model comparison using cross-validation
Models used:
Logistic Regression
Random Forest
XGBoost
LightGBM
Model selection based on PR-AUC for imbalanced data
Performance evaluation after hyperparameter tuning

🔹 Model Performance

Metric	Value
ROC-AUC	0.89
PR-AUC	0.79
Accuracy	78.57%
Recall	79.18%
Precision	47.86%
F1 Score	59.66%

🔹 Key Insights

Unemployed borrowers show the highest default risk
A low credit score significantly increases default probability
High DTI is a strong predictor of default
Recall prioritized to minimize missed defaulters

🔹 Tech Stack

Python (Pandas, NumPy)
Scikit-learn, LightGBM
Streamlit (Dashboard)
Altair (Visualization)

🔹 Business Impact

Enables early identification of high-risk borrowers
Supports data-driven loan approval decisions
Helps reduce potential financial losses
