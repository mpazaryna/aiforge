# src/risk_kit/financial_calculator_mortgage.py


def assess_mortgage_eligibility(annual_income, credit_score, down_payment):
    # Example logic for mortgage eligibility
    home_price = 500000
    required_income = home_price * 0.3  # Example: 30% of home price
    if (
        annual_income < required_income
        or credit_score < 700
        or down_payment < 0.2 * home_price
    ):
        return False  # Not eligible
    return True  # Eligible
