
import argparse
from bigquery_client import get_property_data
from property_profiler import generate_property_overview

def main():
    """
    Main function to run the Property Intelligence Agent.
    """
    parser = argparse.ArgumentParser(description="Property Intelligence Agent")
    parser.add_argument("--street", type=str, required=True, help="Street address of the property")
    parser.add_argument("--zip_code", type=str, required=True, help="Zip code of the property")
    parser.add_argument("--project_id", type=str, help="Google Cloud Project ID. If not provided, it will try to use GOOGLE_CLOUD_PROJECT environment variable.")
    args = parser.parse_args()

    print(f"Searching for property at street: {args.street} and zip code: {args.zip_code}")
    
    property_data = get_property_data(args.street, args.zip_code, args.project_id)

    if property_data is not None:
        overview = generate_property_overview(property_data)
        print(overview)
    else:
        print("Could not retrieve property data.")

if __name__ == "__main__":
    main()
