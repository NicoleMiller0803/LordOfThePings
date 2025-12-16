
import argparse
import json
from deal_memo_generator import generate_deal_memo

def main():
    """
    Main function to run the Deal Memo Agent.
    """
    parser = argparse.ArgumentParser(description="Deal Memo Agent")

    # Property Overview Data
    parser.add_argument("--property_type", type=str, required=True)
    parser.add_argument("--location", type=str, required=True)
    parser.add_argument("--street", type=str, required=True)
    parser.add_argument("--lot_size", type=float, required=True)
    parser.add_argument("--building_size", type=float, required=True)
    parser.add_argument("--unit_config", type=str, required=True)

    # Listing Information
    parser.add_argument("--listing_status", type=str, required=True)
    parser.add_argument("--listing_price", type=float, required=True)

    # Flood & Insurance Risk Assessment
    parser.add_argument("--flood_availability", type=str, required=True)
    parser.add_argument("--flood_premium", type=float, required=True)

    # SAFMR Data
    parser.add_argument("--safmr_data", type=str, required=True)

    # Financial Losses Data
    parser.add_argument("--financial_losses_data", type=str, required=True)
    
    args = parser.parse_args()

    safmr_data = json.loads(args.safmr_data)
    financial_losses_data = json.loads(args.financial_losses_data)

    memo = generate_deal_memo(
        args.property_type, args.location, args.street, args.lot_size, args.building_size, args.unit_config,
        args.listing_status, args.listing_price,
        args.flood_availability, args.flood_premium,
        safmr_data,
        financial_losses_data
    )

    print(memo)

if __name__ == "__main__":
    main()
