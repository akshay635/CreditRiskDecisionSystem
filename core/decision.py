def get_decision(prob, low, high):
    if prob <= low:
        return (
            """The borrower demonstrates a strong financial profile with stable income, a high credit score, \
            and a low debt burden. Default risk is low.\
            ✅ Decision: Approve."""
        )

    elif low < prob <= high:
        return (
            """The borrower shows moderate risk with some inconsistencies in financial behavior and a slightly higher debt burden.\
            Default risk is manageable but requires further assessment.\
            ⚠️ Decision: Review (Manual assessment recommended)."""
        )

    else:
        return (
            """The borrower exhibits high default risk, characterized by weaker financial indicators such as high debt burden \
            or lower credit quality.\
            ❌ Decision: Reject."""
        )
