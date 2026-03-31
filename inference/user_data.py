import streamlit as st 

def load_user_data():
    
    st.sidebar.header("👤 Borrower Details")
    loan_id = str(st.sidebar.text_input('Loan id'))
    name = str(st.sidebar.text_input('Full name'))
    gender = str(st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other']))
    marital_status = str(st.sidebar.selectbox('Marital status', ['Single', 'Married', 'Widowed', 'Divorced']))
    education = str(st.sidebar.selectbox("Education Level", ["Bachelor's", "Master's", "High school", "Phd", "Other"]))
    employment = str(st.sidebar.selectbox("Employment Type", ["Employed", "Self-employed", "Unemployed", "Retired", "Student"]))
    age = int(st.sidebar.slider('Age', 18, 100, 40))
    
    # Validate retired condition
    if employment == "Retired":
        if age < 60:
            st.error("Please enter a valid age (>= 60) if retired.")
        else:
            # Pensioners can still have income, so allow input
            annual_income = st.sidebar.number_input(
                "Annual Pension/Income",
                min_value=50_000,
                max_value=10_000_000,
                value=300_000,
                step=10_000
            )
            monthly_income = round(annual_income / 12, 2)
    
    # Handle unemployed or student
    elif employment in ["Unemployed", "Student"]:
        annual_income = 0
        monthly_income = 0
        st.warning(f"As {employment}, income is set to 0.")
    
    # Handle employed/self-employed
    else:
        annual_income = st.sidebar.slider(
            "Annual Income",
            min_value=100_000,
            max_value=10_000_000,
            value=500_000,
            step=50_000
        )
        monthly_income = round(annual_income / 12, 2)
    
    st.write(f"Annual Income: {annual_income}")
    st.write(f"Monthly Income: {monthly_income}")

    st.sidebar.header("👤 Borrower Credit history details")
    DTI = float(st.sidebar.slider('Debt To Income Ratio', 0.0, 1.0))
    credit_score = int(st.sidebar.slider('Credit Score', 300, 900))
    num_of_open_accounts = int(st.sidebar.slider('Number of open accounts', 0, 20))
    total_credit_limit = float(st.sidebar.number_input('Total available credit limit'))
    current_balance = float(st.sidebar.number_input('Outstanding balance (loan + credit card)'))
    public_records = int(st.sidebar.selectbox('Negative public records (e.g., bankruptcies, legal actions)', options=[0, 1, 2]))
    num_of_delinquencies = int(st.sidebar.slider('Total delinquencies (missed payments)', 0, 12))

    st.sidebar.header("👤 Borrower Loan details")
    loan_amount = float(st.sidebar.number_input('Loan_amount', 1_000.00))
    interest_rate = float(st.sidebar.slider('Interest Rate(%)', 1.0, 25.0))
    loan_term = int(st.sidebar.selectbox('Loan Term', [12, 24, 36, 48, 60]))
    loan_purpose = str(st.sidebar.selectbox("Purpose of the loan", ['Car', 'Debt consolidation', 'Business', 'Other', 
                                                                'Home', 'Medical', 'Education', 'Vacation']))
    
    monthly_rate = (interest_rate/100)/12
    installment = (loan_amount*monthly_rate*(1 + monthly_rate)**loan_term)/((1 + monthly_rate)**loan_term - 1)
    
    loan_income_ratio = round((loan_amount / (annual_income + 1)), 2)
    installment_income_ratio = round((installment / (monthly_income + 1)), 2)
    
    if total_credit_limit <= 0.0:
        credit_utilization = 0.0
    else:
        credit_utilization = (current_balance/total_credit_limit)
        credit_utilization = round(credit_utilization, 2)

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
        'NumOfOpenAccounts': num_of_open_accounts,
        'TotalCreditLimit': total_credit_limit,
        'CurrentBalance': current_balance,
        'PublicRecords': public_records,
        'NumOfDelinquencies': num_of_delinquencies,
        'LoanAmount': float(loan_amount),
        'InterestRate': interest_rate, 
        'LoanTerm': loan_term,
        'LoanPurpose': loan_purpose,
        'Installment': installment,
        'LoanIncomeRatio': loan_income_ratio,
        'InstallmentIncomeRatio': installment_income_ratio,
        'CreditUtilization': credit_utilization
    }
    
    return user_inputs
