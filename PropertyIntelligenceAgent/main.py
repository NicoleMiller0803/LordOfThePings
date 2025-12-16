
import argparse
import json
from bigquery_client import get_property_data, get_comparable_property_data
from property_profiler import generate_property_overview, analyze_comparable_data

def main():
    """
    Main function to run the Property Intelligence Agent.
    """
    parser = argparse.ArgumentParser(description="Property Intelligence Agent")
    parser.add_argument("--street", type=str, required=True, help="Street address of the property")
    parser.add_argument("--zip_code", type=str, required=True, help="Zip code of the property")
    parser.add_argument("--project_id", type=str, help="Google Cloud Project ID. If not provided, it will try to use GOOGLE_CLOUD_PROJECT environment variable.")
    args = parser.parse_args()

    # print(f"Searching for property at street: {args.street} and zip code: {args.zip_code}")
    
    property_data_df = get_property_data(args.street, args.zip_code, args.project_id)

    if property_data_df is not None and not property_data_df.empty:
        prop = property_data_df.iloc[0]
        
        # Get comparable data
        comparable_properties_df = get_comparable_property_data(
            zip_code=prop.get('zip_code'),
            lot_size=prop.get('acre_lot', 0.0),
            building_size=prop.get('house_size', 0.0),
            project_id=args.project_id
        )

        market_analysis = analyze_comparable_data(comparable_properties_df, prop.get('price', 0.0))

        # Combine all data into a single dictionary
        output_data = {
            "property_overview": {
                "property_type": "Single Family Residential (Inferred)", # As previously inferred
                "location": f"{prop.get('city', 'N/A')}, {prop.get('state', 'N/A')}, {str(prop.get('zip_code', 'N/A'))}",
                "street": str(prop.get('street', 'N/A')),
                "lot_size": prop.get('acre_lot', 'N/A'),
                "building_size": prop.get('house_size', 'N/A'),
                "unit_config": f"{prop.get('bed', 'N/A')} Bedrooms, {prop.get('bath', 'N/A')} Bathrooms",
                "listing_status": prop.get('status', 'N/A'),
                "listing_price": prop.get('price', 0.0),
            },
            "comparable_market_value": market_analysis["comparable_market_value"],
            "pricing_assessment": market_analysis["pricing_assessment"]
        }
        print(json.dumps(output_data, indent=4))
    else:
        print(json.dumps({"error": "Could not retrieve property data."}, indent=4))

if __name__ == "__main__":
    main()
