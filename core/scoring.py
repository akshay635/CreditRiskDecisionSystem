def calculate_scores(prob):
    risk_score = int(prob * 100)
    credit_score = int(300 + (1 - prob) * 600)
    return risk_score, credit_score


def get_risk_level(grade):
    risk_map = {
        'A': 'Very Low',
        'B': 'Low',
        'C': 'Medium',
        'D': 'Medium',
        'E': 'High',
        'F': 'Very High'
    }
    return risk_map.get(grade, 'Severe')