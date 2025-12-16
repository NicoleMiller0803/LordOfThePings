
import pandas as pd

def analyze_flood_policy_data(policy_data):
    """
    Analyzes flood policy data to determine insurance availability and estimate premium.

    Args:
        policy_data (pandas.DataFrame): The DataFrame with flood policy data.

    Returns:
        tuple: A tuple containing the insurance availability (str) and estimated premium (float).
    """
    if policy_data is None or policy_data.empty:
        return "Not Available", 0.0

    # Determine Insurance Availability
    availability = "Yes"  # Default
    high_risk_zones = ['A', 'V']
    
    # Check for high-risk zones
    if any(zone in str(policy_data['RatedFloodZones'].iloc[0]) for zone in high_risk_zones):
        availability = "High Risk"
    
    # Check for low policies in force (example threshold: less than 100)
    elif policy_data[' PoliciesinForce '].iloc[0] < 100:
        availability = "Limited"

    # Estimate Annual Premium
    estimated_premium = policy_data['TotalAnnualPayment'].mean()

    return availability, estimated_premium
