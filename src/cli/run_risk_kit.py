#   python src/cli/run_risk_kit.py --calculator mortgage
#   python src/cli/run_risk_kit.py --calculator risk


import argparse
import logging

from risk_kit.calculator_factory import CalculatorFactory  # Import the factory
from risk_kit.logging_config import setup_logging  # Import the logging setup
from risk_kit.utils import train_and_evaluate_model

# Setup logging
setup_logging()  # Call the logging setup function
logging.info("Logging is set up successfully.")  # Test log entry


def main():
    logging.info("Starting the risk assessment model.")  # Basic log entry
    parser = argparse.ArgumentParser(description="Run the risk assessment model.")
    parser.add_argument(
        "--evaluate", action="store_true", help="Evaluate the risk assessment model"
    )
    parser.add_argument(
        "--calculator",
        choices=["risk", "mortgage"],
        required=True,
        help="Type of calculator to use",
    )  # New argument for selecting calculator type
    args = parser.parse_args()

    if args.evaluate:
        logging.info("Starting model evaluation...")
        train_and_evaluate_model()
        logging.info("Model evaluation completed.")

    if args.calculator == "mortgage":
        # Example input values for mortgage assessment
        annual_income = 80000
        credit_score = 720
        down_payment = 100000

        # Use the factory to get the mortgage calculator
        mortgage_calculator = CalculatorFactory.get_calculator("mortgage")
        eligible = mortgage_calculator["assess_mortgage_eligibility"](
            annual_income, credit_score, down_payment
        )
        logging.info(
            f"Mortgage eligibility: {'Eligible' if eligible else 'Not eligible'}"
        )

    elif args.calculator == "risk":
        # Use the factory to get the risk calculator
        risk_calculator = CalculatorFactory.get_calculator("risk")
        # Example usage of risk calculator functions
        data = risk_calculator["generate_data"]()
        classifications = risk_calculator["classify_risk"](data)
        logging.info(f"Risk classifications: {classifications}")


if __name__ == "__main__":
    main()
