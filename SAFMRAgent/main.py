
import argparse
import json
from bigquery_client import get_safmr_data
from safmr_analyzer import analyze_safmr_data

def main():
    """
    Main function to run the SAFMR Agent.
    """
    parser = argparse.ArgumentParser(description="SAFMR Agent for market pricing analysis.")
    parser.add_argument("--zip_code", required=True, help="The zip code of the property.")
    parser.add_argument("--project_id", help="The Google Cloud Project ID.")
    args = parser.parse_args()

    safmr_data = get_safmr_data(args.zip_code, args.project_id)
    analysis = analyze_safmr_data(safmr_data)

    print(json.dumps(analysis, indent=4))

if __name__ == "__main__":
    main()
