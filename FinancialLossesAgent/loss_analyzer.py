
import pandas as pd

def analyze_loss_data(loss_data: pd.DataFrame) -> dict:
    """
    Analyzes the financial loss data and returns a summary.

    Args:
        loss_data (pd.DataFrame): DataFrame containing financial loss data.

    Returns:
        dict: A dictionary containing the financial loss analysis.
    """
    if loss_data is None or loss_data.empty:
        return {"error": "No financial loss data available."}

    record = loss_data.to_dict(orient='records')[0]
    
    closed_with_payment = record.get(' Closed With Payment Losses ', 0)
    open_losses = record.get(' Open Losses ', 0)

    status = "Low"
    if closed_with_payment >= 10 or open_losses >= 5:
        status = "High"
    elif closed_with_payment > 0 or open_losses > 0:
        status = "Medium"

    interpretation = f"The state of {record.get('State', 'N/A')} has a {status.lower()} level of financial loss risk. "
    interpretation += f"There are {closed_with_payment} closed claims with payment and {open_losses} open claims. "
    interpretation += f"The total payments made amount to {record.get(' Total Payments ', 'N/A')}."

    analysis = {
        "status": status,
        "interpretation": interpretation,
        "data": record
    }

    return analysis
