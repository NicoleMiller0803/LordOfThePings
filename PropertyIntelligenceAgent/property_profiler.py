
import pandas as pd

def generate_property_overview(property_data):
    """
    Generates a structured property overview from a pandas DataFrame.

    Args:
        property_data (pandas.DataFrame): The DataFrame with property data.

    Returns:
        str: A formatted string containing the property overview.
    """
    if property_data is None or property_data.empty:
        return "No property data found."

    # Assuming the DataFrame has one row for the property
    prop = property_data.iloc[0]

    street_str = str(prop.get('street', 'N/A'))
    zip_code_str = str(prop.get('zip_code', 'N/A'))

    overview = """
**Property Overview**

**1. Property Identification**
- **Property Type:** {property_type}
- **Location:** {city}, {state}, {zip_code_str}
- **Street:** {street_str}

**2. Physical Characteristics**
- **Lot Size:** {acre_lot} acres
- **Building Size:** {house_size} sq. ft.
- **Unit Configuration (Inferred):**
    - {bed} Bedrooms
    - {bath} Bathrooms

**3. Listing Information**
- **Status:** {status}
- **Listing Price:** ${price:,.2f}
- **Brokered By:** {brokered_by}

**4. Historical Information**
- **Previous Sale Date:** {prev_sold_date}

**5. Data Notes & Inferences**
- **Property Use:** The data suggests this is a residential property. For a commercial loan memo, the intended commercial use (e.g., rental, redevelopment) would need to be specified.
- **Data Fields:** The `street` and `brokered_by` fields may require joining with other data sources for a full picture.
- **Construction/Renovation:** There is no data field indicating the year built or last renovated.
"""
    property_type = "Single Family Residential (Inferred)"  # Placeholder, as it's not in the data

    return overview.format(
        property_type=property_type,
        city=prop.get('city', 'N/A'),
        state=prop.get('state', 'N/A'),
        zip_code_str=zip_code_str,
        street_str=street_str,
        acre_lot=prop.get('acre_lot', 'N/A'),
        house_size=prop.get('house_size', 'N/A'),
        bed=prop.get('bed', 'N/A'),
        bath=prop.get('bath', 'N/A'),
        status=prop.get('status', 'N/A'),
        price=prop.get('price', 0),
        brokered_by=prop.get('brokered_by', 'N/A'),
        prev_sold_date=prop.get('prev_sold_date', 'Not Available')
    )

def analyze_comparable_data(comparable_properties: pd.DataFrame, target_property_price: float) -> dict:
    """
    Analyzes comparable property data to determine a market value and assessment.

    Args:
        comparable_properties (pd.DataFrame): DataFrame containing comparable property data.
        target_property_price (float): The listing price of the target property.

    Returns:
        dict: A dictionary containing the comparable market value and pricing assessment.
    """
    market_analysis = {
        "comparable_market_value": "N/A",
        "pricing_assessment": "Further analysis required to determine if the property is over, under, or fairly priced."
    }

    if comparable_properties is None or comparable_properties.empty:
        market_analysis["comparable_market_value"] = "No comparable properties found."
        market_analysis["pricing_assessment"] = "No comparable properties found to assess pricing."
        return market_analysis

    # Calculate the median listing price of comparable properties
    comparable_prices = comparable_properties['price'].dropna()
    if not comparable_prices.empty:
        median_comp_price = comparable_prices.median()
        market_analysis["comparable_market_value"] = f"${median_comp_price:,.2f}"

        # Assess pricing relative to comparable properties
        if target_property_price < median_comp_price * 0.9: # More than 10% below median
            market_analysis["pricing_assessment"] = "Underpriced (more than 10% below comparable market value)."
        elif target_property_price > median_comp_price * 1.1: # More than 10% above median
            market_analysis["pricing_assessment"] = "Overpriced (more than 10% above comparable market value)."
        elif target_property_price > median_comp_price * 0.95 and target_property_price < median_comp_price * 1.05: # Within 5%
            market_analysis["pricing_assessment"] = "Fairly priced (within 5% of comparable market value)."
        else:
            market_analysis["pricing_assessment"] = "Reasonably priced (within 10% of comparable market value)."
    else:
        market_analysis["comparable_market_value"] = "Comparable properties found, but no valid prices to calculate market value."

    return market_analysis

