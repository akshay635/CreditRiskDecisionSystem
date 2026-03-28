import streamlit as st
import pandas as pd
import importlib
import training.config as config
importlib.reload(config)
from core.model import load_model, predict_pd
from core.scoring import calculate_scores, get_risk_level
from core.decision import get_decision
from core.business import calculate_lgd, expected_loss
from core.explain import get_feature_importance
from inference.user_data import load_user_data
from inference.inference_data_validation import validate_data
from inference.risk_category import GradeSubgrade

def RiskAssessment():
    st.title("🏦 Credit Risk Decision System")
    
    model = load_model()
    
    user_inputs = load_user_data()
    df = pd.DataFrame([user_inputs])
    valid_df = validate_data(df)
    
    st.subheader('Setting up thresholds')
    low = st.slider("Lower Threshold", 0.0, 0.45, 0.30)
    high = st.slider("Higher Threshold", 0.45, 1.0, 0.60)
    
    if st.button("Predict"):
    
        prob = predict_pd(model, valid_df)
    
        # Scores
        risk_score, credit_score = calculate_scores(prob)
        grade = GradeSubgrade(credit_score)
        risk_level = get_risk_level(grade)
    
        # Decision
        decision = get_decision(prob, low, high)
    
        # Business
        lgd = calculate_lgd(valid_df['LoanPurpose'].iloc[0])
        loss = expected_loss(prob, valid_df['LoanAmount'].iloc[0], lgd)
    
        # UI
        st.subheader("📊 Summary")
    
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Probability of Default (PD)", f"{prob:.2%}")
        
        delta = credit_score - valid_df['CreditScore'].iloc[0]
        col2.metric("Credit Score", credit_score, delta)
    
        col3.metric("Expected Loss", f'₹{round(loss)}/-')
    
        col4.metric("Grade", grade)
    
        st.metric("Decision", decision)
        
        st.metric("Risk Level", risk_level)
    
        # Explainability
        features_df = get_feature_importance(model)
    
        with st.expander("Key drivers of the outcome"):
            st.table(features_df.head())
            
            st.bar_chart(features_df.head().set_index('Cleaned_Features'))