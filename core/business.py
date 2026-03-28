def calculate_lgd(purpose):
    lgd_map = {
        'Home': 0.1,
        'Medical': 0.2,
        'Debt Consolidation': 0.3,
        'Other': 0.4,
        'Education': 0.5,
        'Business': 0.6,
        'Car': 0.7,
        'Vacation': 0.8
    }
    return lgd_map.get(purpose.strip().title(), 0.5)


def expected_loss(prob, loan_amount, lgd):
    return round(prob * loan_amount * lgd, 2)