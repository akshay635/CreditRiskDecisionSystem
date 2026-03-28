def get_decision(prob, low, high):
    if prob <= low:
        return "✅ Approve the loan."
    elif prob <= high:
        return "⚠️ Conditional. Manual review recommended."
    else:
        return "❌ Reject the loan"