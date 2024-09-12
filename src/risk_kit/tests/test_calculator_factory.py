# src/risk_kit/tests/test_calculator_factory.py

import pytest

from risk_kit.calculator_factory import CalculatorFactory


def test_calculator_factory():
    # Test for risk calculator
    risk_calculator = CalculatorFactory.get_calculator("risk")
    assert "generate_data" in risk_calculator
    assert "assess_risk" in risk_calculator
    assert "classify_risk" in risk_calculator

    # Test for mortgage calculator
    mortgage_calculator = CalculatorFactory.get_calculator("mortgage")
    assert "assess_mortgage_eligibility" in mortgage_calculator

    # Test for unknown calculator type
    with pytest.raises(ValueError, match="Unknown calculator type: unknown"):
        CalculatorFactory.get_calculator("unknown")
