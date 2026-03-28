import pandas as pd
import streamlit as st
import importlib
import training.config as config
importlib.reload(config)
from app_pages.page1 import RiskAssessment
from app_pages.page2 import PortfolioDashboard
from app_pages.page3 import CreditScoreCalculator
from app_pages.page4 import EMICalculator

st.set_page_config("🏦 Credit Risk Decision System")

page = st.sidebar.selectbox('Select Page', ['Risk Assessment', 'Portfolio Dashboard', 
                                            'Credit Score Calculator', 'EMI Calculator', 'Model Performance metrics'])

if page == 'Risk Assessment':
    RiskAssessment()

elif page == 'Portfolio Dashboard':
    PortfolioDashboard()
    
elif page == 'Credit Score Calculator':
    st.title('💳 Credit Score Calculator')
    payment_history = st.slider('Payment History(%)', 0, 100)
    cu_ratio = st.slider('Credit Utilization ratio', 0.0, 1.0)
    history_years = st.number_input('Credit History(in years)', 0)
    credit_inquiries = st.number_input('No of credit inquiries', 0)
    
    calc = CreditScoreCalculator(payment_history, cu_ratio, history_years, credit_inquiries)
    score = calc.calculate_score()
    st.success(f"Credit Score: {score}")
    
    # To display gauge in Streamlit:
    st.plotly_chart(calc.plot_gauge())

elif page == 'EMI Calculator':
    st.title('💵 EMI Calculator')
    principal = st.number_input('Enter the principal amount')
    if principal < 1000:
        st.error('Please enter valid amount')
    rate = st.slider('Enter the Interest rate(%)', 1.0, 30.0)
    
    if rate < 1.0 and rate > 30.0:
        st.error('Please provide valid interest rate')
        
    tenure = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60])
    emi_calc = EMICalculator(principal, rate, tenure)
    emi = emi_calc.calculate()
    st.subheader(f"EMI: ₹{emi}/-")
    emi_calc.plot(emi)
    
else:
    st.title("📊 Model Performance Dashboard")
    
    cv = pd.read_csv(config.CROSS_VALIDATION)
    confusion_matrix = config.CONFUSION_MATRIX
    metrics = pd.read_csv(config.METRICS)
    
    st.markdown('---')
    st.subheader('Cross-Validation evaluation of machine learning algorithms')
    
    st.dataframe(cv)
    
    best_model = cv['model'].iloc[0]
    best_score = cv['pr_auc'].iloc[0]
    
    st.info(
    f"{best_model} is selected as the final model based on highest PR-AUC "
    f"({best_score:.2f}) during cross-validation.")
    
    st.caption(
    "📌 PR-AUC is used as the primary metric due to class imbalance, "
    "as it better captures performance on the minority (default) class.")
    
    st.markdown('---')
    
    st.subheader("Final Model Performance on Test Dataset")
    
    col1, col2, col3 = st.columns(3) 
    col4, col5, col6 = st.columns(3)
    
    col1.metric("ROC-AUC", f"{metrics['ROC-AUC'].iloc[0]:.2f}")
    col2.metric("PR-AUC ⭐", f"{metrics['PR-AUC'].iloc[0]:.2f}")
    col3.metric("Accuracy", f"{metrics['Accuracy'].iloc[0]:.2%}")
    col4.metric("Precision", f"{metrics['Precision'].iloc[0]:.2%}")
    col5.metric("Recall", f"{metrics['Recall'].iloc[0]:.2%}")
    col6.metric("F1 Score", f"{metrics['F1'].iloc[0]:.2%}")
    
    st.markdown("### 📊 Interpretation")

    st.write(f"""
    - Precision-Recall AUC (PR-AUC) is the primary metric for model selection, \ 
    as it better evaluates performance on the minority class in imbalanced datasets.
    - The model achieves strong discrimination with ROC-AUC of {metrics['ROC-AUC'].iloc[0]:.2f} \
    and PR-AUC of {metrics['PR-AUC'].iloc[0]:.2f}.
    - High recall ({metrics['Recall'].iloc[0]:.2%}) indicates most defaulters are correctly identified.
    - Lower precision ({metrics['Precision'].iloc[0]:.2%}) suggests some false positives, which is acceptable in risk detection.
    """)
    
    
    
    
    