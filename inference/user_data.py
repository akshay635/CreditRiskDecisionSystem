import streamlit as st

def load_user_data():

    st.sidebar.header("👤 Borrower Details")

    loan_id = st.sidebar.text_input('Loan ID')
    name = st.sidebar.text_input('Full Name')

    gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
    marital_status = st.sidebar.selectbox('Marital Status', ['Single', 'Married', 'Widowed', 'Divorced'])
    education = st.sidebar.selectbox("Education Level", ["Bachelor's", "Master's", "High school", "Phd", "Other"])
    age = st.sidebar.slider('Age', 18, 100, 40)

    employment = st.sidebar.selectbox(
        "Employment Type",
        ["Employed", "Self-employed", "Unemployed", "Retired", "Student"]
    )

    # ✅ Validation: Retired condition
    if employment == "Retired" and age < 60:
        st.error("⚠️ Retired individuals should have age ≥ 60")
        st.stop()

    # ✅ Income handling
    if employment in ["Unemployed", "Student"]:
        annual_income = 0.0
        monthly_income = 0.0
        st.warning(f"Income set to 0 for {employment}")
    else:
        annual_income = st.sidebar.slider(
            "Annual Income",
            min_value=100_000,
            max_value=10_000_000,
            value=500_000,
            step=50_000
        )
        monthly_income = round(annual_income / 12, 2)

    st.write(f"Annual Income: ₹{annual_income:,.0f}")
    st.write(f"Monthly Income: ₹{monthly_income:,.0f}")

    # ================= CREDIT DETAILS =================
    st.sidebar.header("📊 Credit Profile")

    DTI = st.sidebar.slider('Debt-to-Income Ratio', 0.0, 1.0, 0.3)
    credit_score = st.sidebar.slider('Credit Score', 300, 900, 650)

    num_open_accounts = st.sidebar.slider('Number of Open Accounts', 0, 20, 5)
    total_credit_limit = st.sidebar.number_input('Total Credit Limit', min_value=0.0)
    current_balance = st.sidebar.number_input('Outstanding Balance', min_value=0.0)

    public_records = st.sidebar.selectbox(
        'Negative Public Records',
        [0, 1, 2]
    )

    num_delinquencies = st.sidebar.slider('Delinquencies', 0, 12, 0)

    # ================= LOAN DETAILS =================
    st.sidebar.header("💰 Loan Details")

    loan_amount = st.sidebar.number_input('Loan Amount', min_value=1000.0)
    interest_rate = st.sidebar.slider('Interest Rate (%)', 1.0, 25.0, 10.0)
    loan_term = st.sidebar.selectbox('Loan Term (months)', [12, 24, 36, 48, 60])

    loan_purpose = st.sidebar.selectbox(
        "Loan Purpose",
        ['Car', 'Debt consolidation', 'Business', 'Other',
         'Home', 'Medical', 'Education', 'Vacation']
    )

    # ================= DERIVED FEATURES =================

    # EMI Calculation (safe)
    monthly_rate = (interest_rate / 100) / 12

    if monthly_rate == 0:
        installment = loan_amount / loan_term
    else:
        installment = (
            loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term
        ) / ((1 + monthly_rate) ** loan_term - 1)

    installment = round(installment, 2)

    # Ratios (avoid division by zero)
    loan_income_ratio = round(loan_amount / (annual_income + 1), 2)
    installment_income_ratio = round(installment / (monthly_income + 1), 2)

    # Credit utilization
    credit_utilization = (
        round(current_balance / total_credit_limit, 2)
        if total_credit_limit > 0 else 0.0
    )

    # ================= OUTPUT =================
    user_inputs = {
        'Age': age,
        'MonthlyIncome': monthly_income,
        'AnnualIncome': float(annual_income),
        'Gender': gender,
        'MaritalStatus': marital_status,
        'EducationLevel': education,
        'EmploymentStatus': employment,
        'DebtToIncomeRatio': DTI,
        'CreditScore': credit_score,
        'NumOfOpenAccounts': num_open_accounts,
        'TotalCreditLimit': total_credit_limit,
        'CurrentBalance': current_balance,
        'PublicRecords': public_records,
        'NumOfDelinquencies': num_delinquencies,
        'LoanAmount': loan_amount,
        'InterestRate': interest_rate,
        'LoanTerm': loan_term,
        'LoanPurpose': loan_purpose,
        'Installment': installment,
        'LoanIncomeRatio': loan_income_ratio,
        'InstallmentIncomeRatio': installment_income_ratio,
        'CreditUtilization': credit_utilization
    }

    return user_inputs
