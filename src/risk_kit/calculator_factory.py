# src/risk_kit/calculator_factory.py

from risk_kit.calculators.finance_assessor import (
    assess_risk,
    classify_risk,
    generate_data,
)
from risk_kit.calculators.finance_mortgage import assess_mortgage_eligibility


class CalculatorFactory:
    @staticmethod
    def get_calculator(calculator_type):
        if calculator_type == "risk":
            return {
                "generate_data": generate_data,
                "assess_risk": assess_risk,
                "classify_risk": classify_risk,
            }
        elif calculator_type == "mortgage":
            return {
                "assess_mortgage_eligibility": assess_mortgage_eligibility,
            }
        else:
            raise ValueError(f"Unknown calculator type: {calculator_type}")
