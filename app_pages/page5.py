import streamlit as st
import plotly.graph_objects as go

class EMICalculator:
    def __init__(self, principal, rate, tenure):
        self.principal = principal
        self.rate = rate
        self.tenure = tenure

    def calculate(self):
        monthly_rate = self.rate / (12 * 100)
        emi = (self.principal * monthly_rate * (1 + monthly_rate) ** self.tenure) / \
              ((1 + monthly_rate) ** self.tenure - 1)
        return round(emi, 2)

    def plot(self, emi):
        total_loan_amount = self.principal + self.principal * (self.rate / 100)
        interest_amount = total_loan_amount - self.principal
        labels = ['Total Loan', 'Principal amount', 'Interest amount']
        values = [total_loan_amount, self.principal, interest_amount]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.3, 0])])
        st.plotly_chart(fig)
