import argparse
import logging
from pathlib import Path

from risk_kit.calculator import CalculatorFactory
from risk_kit.config import config
from risk_kit.utils import train_and_evaluate_model


def main():
    # Setup logging
    config.ensure_directories_exist()
    config.setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting the risk assessment model.")

    parser = argparse.ArgumentParser(description="Run the risk assessment model.")
    parser.add_argument(
        "--evaluate", action="store_true", help="Evaluate the risk assessment model"
    )
    parser.add_argument(
        "--calculator",
        choices=["risk", "mortgage"],
        required=True,
        help="Type of calculator to use",
    )
    args = parser.parse_args()

    if args.evaluate:
        logger.info("Starting model evaluation...")
        train_and_evaluate_model()
        logger.info("Model evaluation completed.")

    if args.calculator == "mortgage":
        # Example input values for mortgage assessment
        annual_income = 80000
        credit_score = 720
        down_payment = 100000

        mortgage_calculator = CalculatorFactory.get_calculator("mortgage")
        eligible = mortgage_calculator["assess_mortgage_eligibility"](
            annual_income, credit_score, down_payment
        )
        logger.info(
            f"Mortgage eligibility: {'Eligible' if eligible else 'Not eligible'}"
        )

    elif args.calculator == "risk":
        risk_calculator = CalculatorFactory.get_calculator("risk")
        data = risk_calculator["generate_data"]()
        classifications = risk_calculator["classify_risk"](data)
        logger.info(f"Risk classifications: {classifications}")

    logger.info("Risk assessment model execution completed.")


if __name__ == "__main__":
    main()
