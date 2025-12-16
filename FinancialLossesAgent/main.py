
import argparse
import json
from bigquery_client import get_financial_loss_data
from loss_analyzer import analyze_loss_data

def main():
    """
    Main function to run the Financial Losses Agent.
    """
    parser = argparse.ArgumentParser(description="Financial Losses Agent for state-level loss trend analysis.")
    parser.add_argument("--state", required=True, help="The state to analyze.")
    parser.add_argument("--project_id", help="The Google Cloud Project ID.")
    args = parser.parse_args()

    loss_data = get_financial_loss_data(args.state, args.project_id)
    analysis = analyze_loss_data(loss_data)

    print(json.dumps(analysis, indent=4))

if __name__ == "__main__":
    main()
