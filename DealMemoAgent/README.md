# Deal Memo Agent

This agent synthesizes information from the `PropertyIntelligenceAgent` and `FloodPolicyAgent` to generate a final deal memo for a potential real estate acquisition.

## Usage

Run the agent from the command line, providing all the required data points from the other agents as arguments.

```bash
python main.py \
    --property_type "Single Family Residential (Inferred)" \
    --location "Gardendale, Texas, 79758" \
    --street "1265166.0" \
    --lot_size 1.28 \
    --building_size 4400.0 \
    --unit_config "7 Bedrooms, 7 Bathrooms" \
    --listing_status "for_sale" \
    --listing_price 470000.00 \
    --flood_availability "High Risk" \
    --flood_premium 26240621.20
```

