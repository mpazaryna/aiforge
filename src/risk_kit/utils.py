import json
import logging
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from .calculators.finance_assessor import classify_risk, generate_data
from .config import config

# Configure logging
logging.basicConfig(filename=config.log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Function to read data from a CSV file
def read_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    return data.to_numpy()  # Convert DataFrame to NumPy array


# Function to write JSON output to a file
def write_json(output, output_path=None):
    output_path = output_path or Path(config.output_json_path)
    logger.info(f"Writing JSON output to: {output_path}")

    try:
        with output_path.open("w") as json_file:
            json.dump(output, json_file, indent=4)
        logger.info(f"JSON output written to {output_path}")
    except Exception as e:
        logger.error(f"Error writing JSON file: {e}")

    return output


# Function to train and evaluate the model
def train_and_evaluate_model(test_size=0.2, random_state=42):
    X = generate_data()
    y = classify_risk(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = LogisticRegression(random_state=random_state)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy}")

    classification_report_dict = classification_report(y_test, y_pred, output_dict=True)

    output = {
        "accuracy": float(accuracy),
        "classification_report": classification_report_dict,
    }

    return write_json(output)
