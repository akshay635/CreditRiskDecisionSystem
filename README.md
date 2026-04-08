# Credit Risk Decision System

🔹 Project Title:

Credit Risk BI Dashboard & ML Decision System

🔹 Overview:

This project is an end-to-end Credit Risk Analytics System that integrates Machine Learning and Business Intelligence dashboards to support loan decision-making.

It predicts borrower default risk and provides both individual-level decisions and portfolio-level insights.

🔹 Objectives: 

Predict Probability of Default (PD) for borrowers
Classify borrowers into risk segments
Support loan approval decisions
Analyze portfolio-level credit risk

🔹 Features:

🔸 Risk Assessment Engine:

Predicts Probability of Default (PD)
Dynamically updates credit score
Segments borrowers into risk categories
Generates decisions: Approve / Review / Reject

🔸 Credit Risk BI Dashboard:

Portfolio KPIs (default rate, income, DTI, etc.)
Risk segmentation:
Employment status
Credit score buckets
DTI buckets
Automated insights highlighting high-risk segments
Borrower distribution analysis

🔸 Financial Tools:

1)Credit score simulator
2)EMI calculator

🔸 Model Performance Dashboard:

Model comparison using cross-validation
Models used:
Logistic Regression
Random Forest
XGBoost
LightGBM
Model selection based on PR-AUC for imbalanced data
Performance evaluation after hyperparameter tuning

🔹 Model Performance:

Metric	Value
ROC-AUC	0.89
PR-AUC	0.79
Accuracy	78.57%
Recall	79.18%
Precision	47.86%
F1 Score	59.66%

🔹 Key Insights:

Unemployed borrowers show the highest default risk
A low credit score significantly increases default probability
High DTI is a strong predictor of default
Recall prioritized to minimize missed defaulters

🔹 Tech Stack:

Python (Pandas, NumPy)
Scikit-learn, LightGBM
Streamlit (Dashboard)
Altair (Visualization)

🔹 Business Impact

Enables early identification of high-risk borrowers
Supports data-driven loan approval decisions
Helps reduce potential financial losses💳 Credit Risk Decision System

An end-to-end Machine Learning system designed to predict the probability of loan default and support data-driven lending decisions.

---

🚀 Live Demo

🔗 https://creditriskdecisionsystem.streamlit.app

---

🎯 Problem Statement

Financial institutions need reliable systems to identify high-risk borrowers and minimize potential losses.
This project focuses on predicting Probability of Default (PD) using borrower financial and behavioral data.

---

🧠 Solution Overview

This system analyzes borrower features such as credit score, income, and debt-to-income ratio to estimate default risk and generate actionable decisions:

- ✅ Approve
- ⚠️ Review
- ❌ Reject

---

⚙️ Key Features

- End-to-end ML pipeline (data preprocessing → modeling → evaluation → deployment)
- Handles imbalanced data using recall and PR-AUC focused evaluation
- Real-time prediction using Streamlit interface
- Risk segmentation based on probability thresholds
- Business-aligned decision logic

---

📊 Model Performance

- ROC-AUC: 0.89
- PR-AUC: 0.79
- Recall: 79% (focused on identifying high-risk borrowers)

---

🛠️ Tech Stack

- Programming: Python, SQL
- ML Libraries: Scikit-learn, XGBoost, LightGBM
- Data Processing: Pandas, NumPy
- Visualization: Matplotlib, Seaborn
- Deployment: Streamlit
- Version Control: Git, GitHub

---

🔄 ML Workflow

1. Data Extraction & Validation
2. Data Cleaning & Feature Engineering
3. Train-Test Split (Stratified)
4. Model Training & Evaluation
5. Hyperparameter Tuning
6. Final Model Selection
7. Deployment using Streamlit

---

💡 Key Learnings

- Handling imbalanced data requires focusing on recall and PR-AUC rather than accuracy
- Feature engineering and domain understanding significantly impact model performance
- Probability-based decision systems are more practical than binary predictions

---

🚀 Future Improvements

- Deploy model as REST API using FastAPI
- Add model monitoring and drift detection
- Integrate explainability (SHAP values)
- Enhance UI/UX for better user experience

---

👤 Author

Akshay Atanure
Machine Learning Engineer | Data Science | Credit Risk Analytics

📧 akshayatanure11@gmail.com
🔗 LinkedIn | GitHub

---

⭐ If you found this project useful, feel free to star the repository!
