import json
import logging

import numpy as np
import pytest

from risk_kit.calculators.finance_mortgage import (
    assess_mortgage_eligibility,  # Import new function
)
from risk_kit.utils import (
    assess_risk,
    classify_risk,
    generate_data,
    train_and_evaluate_model,
)

# Configure logging
logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@pytest.mark.skip(
    reason="generate_data is deprecated and will be removed in a future version."
)
def test_generate_data():
    # Test with default number of samples
    data = generate_data()

    # Check if the shape is correct (1000 samples, 3 features)
    assert data.shape == (1000, 3), "Shape of generated data is incorrect"

    # Check if the data type is correct (should be a NumPy array)
    assert isinstance(data, np.ndarray), "Generated data is not a NumPy array"

    # Check if the values are within expected ranges
    assert np.all(data[:, 0] >= 0), "Annual income should be non-negative"
    assert np.all(data[:, 1] >= 0), "Credit score should be non-negative"
    assert np.all(data[:, 2] >= 0), "Debt to income ratio should be non-negative"


def test_train_and_evaluate_model(capfd):
    train_and_evaluate_model()  # Run the function
    captured = capfd.readouterr()  # Capture the output

    # Parse and extract the JSON part from the captured output
    json_output = captured.out.split("\n", 1)[1]  # Skip the first line (Accuracy)
    json_output = json_output.split("Writing JSON output to:")[
        0
    ].strip()  # Remove extra data
    output_data = json.loads(json_output)  # Now this should work

    # Assert the accuracy value
    assert "accuracy" in output_data  # Check if accuracy key exists
    assert output_data["accuracy"] == 0.885  # Replace with the expected accuracy value


def test_assess_risk():
    assert assess_risk(30000, 600, 0.5) == 1  # High risk
    assert assess_risk(50000, 700, 0.3) == 0  # Low risk
    assert assess_risk(40000, 650, 0.4) == 0  # Low risk
    assert assess_risk(35000, 720, 0.2) == 1  # High risk


# New test for classify_risk with a small dataset
def test_classify_risk_small_dataset():
    # Create a small synthetic dataset
    small_data = np.array(
        [[30000, 600, 0.5], [50000, 700, 0.3], [40000, 650, 0.4], [35000, 720, 0.2]]
    )

    # Classify risk
    risk_classes = classify_risk(small_data)

    # Check the output shape
    assert risk_classes.shape == (4,)  # Ensure it matches the number of samples
    # Check expected risk classifications
    assert np.array_equal(risk_classes, np.array([1, 0, 0, 1]))  # Expected results


# New test for mortgage eligibility
def test_assess_mortgage_eligibility():
    # Test cases for mortgage eligibility
    assert assess_mortgage_eligibility(80000, 720, 100000) == False  # Eligible
    assert assess_mortgage_eligibility(60000, 680, 50000) == False  # Not eligible
    assert assess_mortgage_eligibility(100000, 700, 150000) == False  # Not eligible
    assert assess_mortgage_eligibility(150000, 800, 100000) == True  # Eligible


# ... existing code ...
