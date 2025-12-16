
import argparse
from bigquery_client import get_flood_policy_data
from flood_policy_analyzer import analyze_flood_policy_data

def main():
    """
    Main function to run the Flood Policy Agent.
    """
    parser = argparse.ArgumentParser(description="Flood Policy Agent")
    parser.add_argument("--state", type=str, required=True, help="State of the property (e.g., 'FL')")
    parser.add_argument("--coverage_type", type=str, required=True, help="Coverage type (e.g., 'Residential')")
    parser.add_argument("--project_id", type=str, help="Google Cloud Project ID. If not provided, it will try to determine it automatically.")
    args = parser.parse_args()

    print(f"Searching for flood policy data in {args.state} for {args.coverage_type} properties.")
    
    policy_data = get_flood_policy_data(args.state, args.coverage_type, args.project_id)

    if policy_data is not None:
        availability, premium = analyze_flood_policy_data(policy_data)
        print(f"Insurance Availability: {availability}")
        print(f"Estimated Annual Premium: ${premium:,.2f}")
    else:
        print("Could not retrieve flood policy data.")

if __name__ == "__main__":
    main()
