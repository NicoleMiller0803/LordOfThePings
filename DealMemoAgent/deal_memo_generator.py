
def _safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 'N/A'

def generate_deal_memo(
    # Property Overview Data
    property_type, location, street, lot_size, building_size, unit_config,
    # Listing Information
    listing_status, listing_price,
    # Flood & Insurance Risk Assessment
    flood_availability, flood_premium,
    # SAFMR Data
    safmr_data,
    # Financial Losses Data
    financial_losses_data
):
    """
    Generates a structured deal memo from the provided data.
    """

    # Basic recommendation logic
    recommendation = "Buy"
    if flood_availability == "High Risk":
        recommendation = "Buy with Conditions"
    if flood_availability == "Not Available":
        recommendation = "Pass"

    safmr_analysis = ""
    if isinstance(safmr_data, list) and safmr_data:
        # Sort by year in descending order to get the most recent data first
        safmr_data.sort(key=lambda x: x.get('year', 0), reverse=True)
        record = safmr_data[0] # Get the most recent record

        safmr_analysis += f"- **{record.get('program_name', 'N/A')} ({record.get('year', 'N/A')})**\n"
        fmr_1 = _safe_float(record.get('safmr1br', 'N/A'))
        fmr_2 = _safe_float(record.get('safmr2br', 'N/A'))
        fmr_3 = _safe_float(record.get('safmr3br', 'N/A'))
        fmr_4 = _safe_float(record.get('safmr4br', 'N/A'))

        safmr_analysis += f"  - FMR for 1-Bedroom: ${fmr_1:,.2f}\n" if isinstance(fmr_1, float) else "  - FMR for 1-Bedroom: N/A\n"
        safmr_analysis += f"  - FMR for 2-Bedroom: ${fmr_2:,.2f}\n" if isinstance(fmr_2, float) else "  - FMR for 2-Bedroom: N/A\n"
        safmr_analysis += f"  - FMR for 3-Bedroom: ${fmr_3:,.2f}\n" if isinstance(fmr_3, float) else "  - FMR for 3-Bedroom: N/A\n"
        safmr_analysis += f"  - FMR for 4-Bedroom: ${fmr_4:,.2f}\n" if isinstance(fmr_4, float) else "  - FMR for 4-Bedroom: N/A\n"
    else:
        safmr_analysis = "[No SAFMR data available.]"

    financial_loss_analysis = ""
    if isinstance(financial_losses_data, dict) and 'status' in financial_losses_data:
        financial_loss_analysis += f"- **State-Level Financial Loss Risk:** {financial_losses_data.get('status', 'N/A')}\n"
        financial_loss_analysis += f"  - {financial_losses_data.get('interpretation', '')}\n"
    else:
        financial_loss_analysis = "[No financial loss data available.]"


    memo = f"""
# Deal Memo

## Executive Summary
This memo provides a summary and recommendation for the potential acquisition of the property located at {street}, {location}.
Based on the available data, the preliminary recommendation is to **{recommendation}**.

## Property Overview
- **Property Type:** {property_type}
- **Location:** {location}
- **Street:** {street}
- **Lot Size:** {lot_size} acres
- **Building Size:** {building_size} sq. ft.
- **Unit Configuration:** {unit_config}

## Market & Pricing Analysis
- **Listing Price:** ${listing_price:,.2f}
- **Small Area Fair Market Rents (SAFMR):**
{safmr_analysis}

## Flood & Insurance Risk Assessment
- **Insurance Availability:** {flood_availability}
- **Estimated Annual Flood Premium:** ${flood_premium:,.2f}

## Mitigation Strategies
- **Flood Risk:** If the property is in a high-risk flood zone, mitigation strategies could include obtaining a comprehensive flood insurance policy, implementing flood-proofing measures, or challenging the flood zone designation.
- **Market Risk:** {financial_loss_analysis}

## Investment Recommendation
**{recommendation}**

- **Justification:** The recommendation is based on the preliminary data. A 'Buy' recommendation is contingent on a clean due diligence report. A 'Buy with Conditions' is recommended when there are identifiable risks (like flood risk) that need to be addressed before closing. A 'Pass' is recommended when the risks are deemed too high or the data is incomplete.
"""
    return memo
