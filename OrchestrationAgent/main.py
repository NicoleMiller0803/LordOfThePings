
import argparse
import subprocess
import re
import json

def run_property_intelligence_agent(street, zip_code, project_id):
    """Runs the PropertyIntelligenceAgent and returns its output."""
    command = [
        "python3", "PropertyIntelligenceAgent/main.py",
        "--street", street,
        "--zip_code", zip_code,
        "--project_id", project_id
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return json.dumps({"error": f"PropertyIntelligenceAgent failed: {result.stderr.strip()}"})
    return result.stdout

def run_flood_policy_agent(state, coverage_type, project_id):
    """Runs the FloodPolicyAgent and returns its output."""
    command = [
        "python3", "FloodPolicyAgent/main.py",
        "--state", state,
        "--coverage_type", coverage_type,
        "--project_id", project_id
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FloodPolicyAgent failed: {result.stderr}")
    return result.stdout

def run_safmr_agent(zip_code, project_id):
    """Runs the SAFMRAgent and returns its output."""
    command = [
        "python3", "SAFMRAgent/main.py",
        "--zip_code", zip_code,
        "--project_id", project_id
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"SAFMRAgent failed: {result.stderr}")
    return result.stdout

def run_financial_losses_agent(state, project_id):
    """Runs the FinancialLossesAgent and returns its output."""
    command = [
        "python3", "FinancialLossesAgent/main.py",
        "--state", state,
        "--project_id", project_id
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FinancialLossesAgent failed: {result.stderr}")
    return result.stdout

def run_deal_memo_agent(property_data, flood_data, safmr_data, financial_losses_data):
    """Runs the DealMemoAgent with the combined data."""
    if "error" in property_data:
        raise Exception(f"Property Intelligence Agent returned an error: {property_data['error']}")
    
    command = [
        "python3", "DealMemoAgent/main.py",
        "--property_type", property_data['property_overview']['property_type'],
        "--location", property_data['property_overview']['location'],
        "--street", property_data['property_overview']['street'],
        "--lot_size", str(property_data['property_overview']['lot_size']),
        "--building_size", str(property_data['property_overview']['building_size']),
        "--unit_config", property_data['property_overview']['unit_config'],
        "--listing_status", property_data['property_overview']['listing_status'],
        "--listing_price", str(property_data['property_overview']['listing_price']),
        "--comparable_market_value", property_data['comparable_market_value'],
        "--pricing_assessment", property_data['pricing_assessment'],
        "--flood_availability", flood_data['flood_availability'],
        "--flood_premium", str(flood_data['flood_premium']),
        "--safmr_data", json.dumps(safmr_data),
        "--financial_losses_data", json.dumps(financial_losses_data)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"DealMemoAgent failed: {result.stderr}")
    return result.stdout

def parse_property_data(output):
    """
    Parses the output of the PropertyIntelligenceAgent, attempting to extract a JSON object.
    It handles cases where non-JSON text might precede or follow the actual JSON.
    """
    json_match = re.search(r'(\{.*\})', output, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            return data
        except json.JSONDecodeError:
            pass # Fall through to error case
    
    return {"error": f"Invalid or no JSON object found in PropertyIntelligenceAgent output: {output.strip()}"}


def parse_flood_data(output):
    """Parses the output of the FloodPolicyAgent."""
    data = {
        'flood_availability': 'N/A',
        'flood_premium': 0.0
    }
    
    availability_match = re.search(r"Insurance Availability:\s*(.*)", output)
    if availability_match:
        data['flood_availability'] = availability_match.group(1).strip()
    else:
        # Fallback if the pattern is not found, or if there's an error in output
        if "Error:" in output:
            data['flood_availability'] = f"Error from FloodPolicyAgent: {output.strip()}"

    premium_match = re.search(r"Estimated Annual Premium:\s*\$(.*)", output)
    if premium_match:
        try:
            data['flood_premium'] = float(premium_match.group(1).replace(',', '').strip())
        except ValueError:
            data['flood_premium'] = 0.0 # Default if premium is not a valid number

    return data

def parse_safmr_data(output):
    """Parses the output of the SAFMRAgent."""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON output from SAFMRAgent"}

def parse_financial_losses_data(output):
    """Parses the output of the FinancialLossesAgent."""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON output from FinancialLossesAgent"}

def parse_deal_memo_data(output):
    """Parses the JSON output of the DealMemoAgent."""
    try:
        data = json.loads(output)
        return data
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON output from DealMemoAgent: {output.strip()}"}

def main():
    """Main function to run the Orchestration Agent."""
    parser = argparse.ArgumentParser(description="Orchestration Agent")
    parser.add_argument("--street", type=str, required=True)
    parser.add_argument("--zip_code", type=str, required=True)
    parser.add_argument("--state", type=str, required=True)
    parser.add_argument("--coverage_type", type=str, required=True)
    parser.add_argument("--project_id", type=str, required=True)
    args = parser.parse_args()

    property_output = run_property_intelligence_agent(args.street, args.zip_code, args.project_id)
    property_data = parse_property_data(property_output)
    
    flood_output = run_flood_policy_agent(args.state, args.coverage_type, args.project_id)
    flood_data = parse_flood_data(flood_output)

    safmr_output = run_safmr_agent(args.zip_code, args.project_id)
    safmr_data = parse_safmr_data(safmr_output)

    financial_losses_output = run_financial_losses_agent(args.state, args.project_id)
    financial_losses_data = parse_financial_losses_data(financial_losses_output)

    deal_memo_json_str = run_deal_memo_agent(property_data, flood_data, safmr_data, financial_losses_data)
    deal_memo_data = parse_deal_memo_data(deal_memo_json_str)

    # Output the structured JSON
    print(json.dumps(deal_memo_data, indent=4))

if __name__ == "__main__":
    main()