# 💳 Credit Risk Decision System for Loan Default Prediction and NPA reduction

An end-to-end Machine Learning + Business Intelligence system to predict Probability of Default (PD) and support data-driven loan decisions.

---

🚀 Live App

🔗 https://creditriskdecisionsystem.streamlit.app

---

📸 Screenshots

🔹 Risk Prediction Interface

<img width="1892" height="907" alt="image" src="https://github.com/user-attachments/assets/a58efedd-6fde-4817-96b3-38420dc9abe4" />

🔹 BI Dashboard

<img width="1902" height="905" alt="image" src="https://github.com/user-attachments/assets/0fd939d9-4389-4b74-a7f3-6720ec0c7272" />


---

� Problem Statement

Banks and NBFCs face rising NPAs (Non Performing Assets) due to irregular payments, borrower bankruptcies, poor creditworthiness, and financial distress. These defaults lead to significant financial and revenue losses for BFSI institutions.

---

🎯 Goal:

Develop a machine learning system to estimate the probability of loan default using borrower personal, financial, loan, and credit data. Segment borrowers into risk tiers (low, medium, high) to enable proactive interventions and reduce NPAs.

---

💾 Dataset Sources:

•	Loan application records (demographics, employment, income).

•	Credit bureau data (credit scores, repayment history).

•	Loan transaction data (amount, tenure, EMI).

•	Macroeconomic indicators (optional enrichment)

---

🧠 Solution Overview

The system analyzes borrower features such as credit score, income, and debt-to-income ratio to estimate default probability and generate decisions:

- ✅ Approve
- ⚠️ Review
- ❌ Reject

It combines ML predictions + business logic + portfolio insights.

---

⚙️ Key Features

🔹 Risk Assessment Engine

- Predicts Probability of Default (PD)
- Dynamic risk scoring
- Borrower segmentation
- Decision engine (Approve / Review / Reject)

---

📊 BI Dashboard

- Portfolio KPIs (default rate, income, DTI)
- Risk segmentation:
  - Credit score buckets
  - DTI buckets
  - Employment status
- Automated insights
- Distribution analysis

---

💡 Financial Tools

- Credit Score Simulator
 
<img width="1888" height="903" alt="image" src="https://github.com/user-attachments/assets/62aa709f-54e5-4477-b577-d14f0617b4e9" />

- EMI Calculator

<img width="1902" height="910" alt="image" src="https://github.com/user-attachments/assets/71dc641f-fe10-4783-bca2-f8a9194486df" />

---

📊 Model Performance

<img width="1893" height="827" alt="image" src="https://github.com/user-attachments/assets/76714702-3fa6-4efd-b912-36aabcb89f91" />

- ROC-AUC: 0.89
- PR-AUC: 0.79
- Recall: 79%
  
📈 Business Impact 

- The LightGBM model is the top-performing solution, delivering superior Precision-Recall Score and F1-score compared to other models. Most importantly, it achieves a recall rate of ~80%, meaning it successfully identifies 8 out of 10 defaulters.

- For example, in a portfolio of 100 new borrowers where 40 are actual defaulters, LightGBM correctly flags around 32 default cases. This translates into a 20% false negative rate, significantly reducing undetected defaulters compared to baseline models.

- From a financial perspective, this performance directly lowers expected losses. Assuming an average loss of ₹X per default, LightGBM reduces potential losses by 80% of the total default exposure. In other words, the model not only improves predictive accuracy but also reduces the financial loss rate by catching the majority of high-risk borrowers before loan disbursement.

---

🏗️ System Architecture

Data → Validation → Feature Engineering → ML Model → Probability → Decision Engine → Streamlit App

---

🛠️ Tech Stack

- Python, SQL
- Scikit-learn, XGBoost, LightGBM
- Pandas, NumPy
- Matplotlib, Seaborn
- Streamlit
- Git & GitHub

---

🔄 ML Workflow

1. Data Extraction & Validation
2. Data Cleaning & Feature Engineering
3. Train-Test Split (Stratified)
4. Model Training & Evaluation
5. Hyperparameter Tuning
6. Final Model Selection
7. Deployment

---

💡 Key Learnings

- Imbalanced data requires Recall & PR-AUC focus
- Feature engineering drives performance
- Probability-based systems improve decision-making

---

🚀 Future Improvements

- FastAPI deployment (production-ready API)
- Model monitoring & drift detection
- Explainability (SHAP)
- UI enhancements

---

👤 Author

Akshay Atanure

Machine Learning Engineer | Data Science | Credit Risk Analytics

📧 akshayatanure11@gmail.com
🔗 LinkedIn | GitHub

---

⭐ If you found this project useful, consider giving it a star!
