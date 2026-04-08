import plotly.graph_objects as go

class CreditScoreCalculator:
    def __init__(self, payment_history, utilization, history_years, inquiries):
        self.payment_history = payment_history
        self.utilization = utilization
        self.history_years = history_years
        self.inquiries = inquiries

    def normalize_features(self):
        """Normalize all features to [0,1] scale."""
        PH_norm = self.payment_history / 100
        CU_norm = 1 - self.utilization
        LH_norm = min(self.history_years, 20) / 20
        NC_norm = 1 - min(self.inquiries, 10) / 10
        return PH_norm, CU_norm, LH_norm, NC_norm

    def calculate_score(self):
        """Calculate credit score using weighted formula."""
        PH_norm, CU_norm, LH_norm, NC_norm = self.normalize_features()
        score = 300 + 550 * (0.40 * PH_norm + 0.30 * CU_norm + 0.20 * LH_norm + 0.10 * NC_norm)
        return round(score)

    def plot_gauge(self):
        """Return a Plotly gauge chart for visualization."""
        score = self.calculate_score()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Credit Score"},
            gauge={
                'axis': {'range': [300, 850]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [300, 550], 'color': "red"},
                    {'range': [550, 650], 'color': "orange"},
                    {'range': [650, 750], 'color': "yellow"},
                    {'range': [750, 850], 'color': "green"}
                ],
            }
        ))
        return fig

