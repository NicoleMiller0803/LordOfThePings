
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

