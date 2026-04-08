import streamlit as st
import pandas as pd
from PIL import Image
import importlib
import training.config as config
importlib.reload(config)

def ModelDashboard():
    st.title("📊 Model Performance Dashboard")
    st.caption("📌 Metrics are calculated at decision threshold = 0.45")
    # -------------------------------
    # Load Artifacts
    # -------------------------------
    cv = pd.read_csv(config.CROSS_VALIDATION)
    metrics = pd.read_csv(config.METRICS)

    # -------------------------------
    # Cross Validation Results
    # -------------------------------
    st.subheader("Model Comparison (Cross-Validation Results)")
    st.dataframe(cv)

    best_model = cv["model"].iloc[0]
    best_score = cv["pr_auc"].iloc[0]

    st.info(
        f"{best_model} is selected as the final model based on the highest PR-AUC "
        f"({best_score:.2f}) during cross-validation."
    )

    st.caption(
        "📌 PR-AUC is used as the primary metric due to class imbalance, "
        "capturing performance on the minority (default) class more effectively."
    )

    st.markdown("---")

    # ------------------------------
    # Test Performance
    # -------------------------------
    st.subheader("Final Model Performance on Test Dataset")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("ROC-AUC", f"{metrics['ROC-AUC'].iloc[0]:.2f}")
    col2.metric("PR-AUC ⭐", f"{metrics['PR-AUC'].iloc[0]:.2f}")
    col3.metric("Accuracy", f"{metrics['Accuracy'].iloc[0]:.2%}")

    col4.metric("Precision", f"{metrics['Precision'].iloc[0]:.2%}")
    col5.metric("Recall", f"{metrics['Recall'].iloc[0]:.2%}")
    col6.metric("F1 Score", f"{metrics['F1'].iloc[0]:.2%}")

    # ------------------------------
    # Confusion Matrix
    # -------------------------------

    st.markdown("---")
    # Displaying the confusion matrix
    st.subheader('Confusion Matrix')

    confusion_matrix = Image.open(config.CONFUSION_MATRIX)
    
    # Display the image with a caption
    st.image(confusion_matrix, caption="Confusion Matrix", use_column_width=True)
    st.info('Top left shows True Negatives, bottom left shows False Negatives, top right shows False Positives and bottom right shows True Positives')
    st.markdown("---")

    # -------------------------------
    # Interpretation
    # -------------------------------
    st.markdown("### 📊 Interpretation")

    st.write(f"""
    - PR-AUC is the primary metric for model selection due to class imbalance.
    - The model achieves strong discrimination with ROC-AUC of {metrics['ROC-AUC'].iloc[0]:.2f} 
      and PR-AUC of {metrics['PR-AUC'].iloc[0]:.2f}.
    - High recall ({metrics['Recall'].iloc[0]:.2%}) ensures most defaulters are correctly identified.
    - Lower precision ({metrics['Precision'].iloc[0]:.2%}) indicates some false positives, 
      which is acceptable in credit risk scenarios.
    """)
