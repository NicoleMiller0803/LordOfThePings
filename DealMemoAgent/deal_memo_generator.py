
import json

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
    # Comparable Market Analysis
    comparable_market_value, pricing_assessment,
    # Flood & Insurance Risk Assessment
    flood_availability, flood_premium,
    # SAFMR Data
    safmr_data,
    # Financial Losses Data
    financial_losses_data
):
    """
    Generates a structured deal memo from the provided data as a JSON object.
    """

    # Basic recommendation logic
    recommendation = "Buy"
    if flood_availability == "High Risk":
        recommendation = "Buy with Conditions"
    elif flood_availability == "Not Available":
        recommendation = "Pass"

    safmr_details = []
    if isinstance(safmr_data, list) and safmr_data:
        safmr_data.sort(key=lambda x: x.get('year', 0), reverse=True)
        record = safmr_data[0] # Get the most recent record

        fmr_1 = _safe_float(record.get('safmr1br', 'N/A'))
        fmr_2 = _safe_float(record.get('safmr2br', 'N/A'))
        fmr_3 = _safe_float(record.get('safmr3br', 'N/A'))
        fmr_4 = _safe_float(record.get('safmr4br', 'N/A'))

        safmr_details.append({
            "program_name": record.get('program_name', 'N/A'),
            "year": record.get('year', 'N/A'),
            "fmr_1_bedroom": fmr_1 if isinstance(fmr_1, float) else 'N/A',
            "fmr_2_bedroom": fmr_2 if isinstance(fmr_2, float) else 'N/A',
            "fmr_3_bedroom": fmr_3 if isinstance(fmr_3, float) else 'N/A',
            "fmr_4_bedroom": fmr_4 if isinstance(fmr_4, float) else 'N/A',
        })
    
    financial_loss_status = "N/A"
    financial_loss_interpretation = "No financial loss data available."
    if isinstance(financial_losses_data, dict) and 'status' in financial_losses_data:
        financial_loss_status = financial_losses_data.get('status', 'N/A')
        financial_loss_interpretation = financial_losses_data.get('interpretation', '')


    deal_memo_data = {
        "executive_summary": {
            "location": f"{street}, {location}",
            "recommendation": recommendation,
            "justification": "The recommendation is based on the preliminary data. A 'Buy' recommendation is contingent on a clean due diligence report. A 'Buy with Conditions' is recommended when there are identifiable risks (like flood risk) that need to be addressed before closing. A 'Pass' is recommended when the risks are deemed too high or the data is incomplete."
        },
        "property_overview": {
            "property_type": property_type,
            "location": location,
            "street": street,
            "lot_size": f"{lot_size} acres",
            "building_size": f"{building_size} sq. ft.",
            "unit_config": unit_config
        },
        "market_pricing_analysis": {
            "listing_price": listing_price,
            "comparable_market_value": comparable_market_value,
            "pricing_assessment": pricing_assessment,
            "safmr_data": safmr_details
        },
        "flood_insurance_risk_assessment": {
            "insurance_availability": flood_availability,
            "estimated_annual_premium": flood_premium
        },
        "mitigation_strategies": {
            "flood_risk": "If the property is in a high-risk flood zone, mitigation strategies could include obtaining a comprehensive flood insurance policy, implementing flood-proofing measures, or challenging the flood zone designation.",
            "market_risk": financial_loss_interpretation # Use the interpretation here
        },
        "investment_recommendation": {
            "recommendation": recommendation,
            "status_color": recommendation.lower().replace(' ', '-') # For UI coloring
        },
        "financial_loss_risk": {
            "status": financial_loss_status,
            "interpretation": financial_loss_interpretation,
            "status_color": financial_loss_status.lower().replace(' ', '-') # For UI coloring
        }
    }
    return json.dumps(deal_memo_data, indent=4)
