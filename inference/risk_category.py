# risk categories created using Probability of Default
def GradeSubgrade(credit_score):
    if credit_score >= 800:
        return 'A'
    elif 700 <= credit_score < 800:
        return 'B'
    elif 600 <= credit_score < 700:
        return 'C' 
    elif 500 <= credit_score < 600:
        return 'D'
    elif 400 <= credit_score < 500: 
        return 'E'
    else:
        return 'F'