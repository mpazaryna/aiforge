import json
import logging
import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from .calculators.finance_assessor import (  # Import financial calculations
    assess_risk,
    classify_risk,
    generate_data,
)
from .config import (  # Import DATA_DIRECTORY
    LOGGING_FILENAME,
    LOGGING_LEVEL,
    OUTPUT_JSON_FILENAME,
    config,
)

# Configure logging
logging.basicConfig(filename=config.log_file, level=logging.DEBUG)


# Function to read data from a CSV file
def read_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    return data.to_numpy()  # Convert DataFrame to NumPy array


# Function to write JSON output to a file
def write_json(output):
    json_output = json.dumps(output, indent=4)  # Convert output to JSON format
    logger.info(f"JSON output: {json_output}")

    output_path = Path(config.output_json_path)
    logger.info(f"Writing JSON output to: {output_path}")

    try:
        with output_path.open("w") as json_file:
            json_file.write(json_output)
            json_file.write("\n")
        logger.info(f"JSON output written to {output_path}")
    except Exception as e:
        logger.error(f"Error writing JSON file: {e}")

    return output  # Return the output for consistency


# Function to train and evaluate the model
def train_and_evaluate_model():
    # Generate and prepare data
    X = generate_data()
    y = classify_risk(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train logistic regression model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")  # Ensure this line is present

    # Get classification report as a dictionary
    classification_report_dict = classification_report(
        y_test, y_pred, output_dict=True
    )  # Modify this line

    # Prepare output in JSON format
    output = {
        "accuracy": float(accuracy),  # Convert to float to ensure JSON serialization
        "classification_report": classification_report_dict,
    }

    # Add debug information
    logging.info(f"Type of config: {type(config)}")
    logging.info(f"Dir of config: {dir(config)}")

    write_json(output)
    return output
