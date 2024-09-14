import json
import logging
import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from risk_kit.config import LOGGING_FILENAME, LOGGING_LEVEL  # Import DATA_DIRECTORY

# Configure logging
logging.basicConfig(filename=LOGGING_FILENAME, level=LOGGING_LEVEL)


# Generate synthetic data
def generate_data(n_samples=1000):
    warnings.warn(
        "generate_data is deprecated and will be removed in a future version.",
        DeprecationWarning,
    )
    np.random.seed(42)
    annual_income = np.random.normal(50000, 15000, n_samples)
    credit_score = np.random.normal(700, 50, n_samples)

    # Ensure the debt-to-income ratio is non-negative
    debt_to_income_ratio = np.random.rand(
        1000
    )  # Example logic, replace with your actual logic
    # Ensure values are non-negative
    debt_to_income_ratio = np.abs(
        debt_to_income_ratio
    )  # Make sure values are non-negative

    data = np.column_stack((annual_income, credit_score, debt_to_income_ratio))
    return data


# Function to assess risk based on individual parameters
def assess_risk(annual_income, credit_score, debt_to_income):
    if annual_income < 40000 or credit_score < 650 or debt_to_income > 0.4:
        return 1  # High risk
    return 0  # Low risk


# Create risk classification using assess_risk
def classify_risk(data):
    return np.array([assess_risk(row[0], row[1], row[2]) for row in data])
