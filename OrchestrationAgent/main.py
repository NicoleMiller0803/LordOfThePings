
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
        raise Exception(f"PropertyIntelligenceAgent failed: {result.stderr}")
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
    command = [
        "python3", "DealMemoAgent/main.py",
        "--property_type", property_data['property_type'],
        "--location", property_data['location'],
        "--street", property_data['street'],
        "--lot_size", str(property_data['lot_size']),
        "--building_size", str(property_data['building_size']),
        "--unit_config", property_data['unit_config'],
        "--listing_status", property_data['listing_status'],
        "--listing_price", str(property_data['listing_price']),
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
    """Parses the output of the PropertyIntelligenceAgent."""
    data = {}
    data['property_type'] = re.search(r"\*\*Property Type:\*\* (.*)", output).group(1)
    data['location'] = re.search(r"\*\*Location:\*\* (.*)", output).group(1)
    data['street'] = re.search(r"\*\*Street:\*\* (.*)", output).group(1)
    data['lot_size'] = float(re.search(r"\*\*Lot Size:\*\* (.*) acres", output).group(1))
    data['building_size'] = float(re.search(r"\*\*Building Size:\*\* (.*) sq. ft.", output).group(1))
    
    bedrooms_match = re.search(r"(\d+) Bedrooms", output)
    bathrooms_match = re.search(r"(\d+) Bathrooms", output)
    data['unit_config'] = f"{bedrooms_match.group(1) if bedrooms_match else 'N/A'} Bedrooms, {bathrooms_match.group(1) if bathrooms_match else 'N/A'} Bathrooms"

    data['listing_status'] = re.search(r"\*\*Status:\*\* (.*)", output).group(1)
    data['listing_price'] = float(re.search(r"\*\*Listing Price:\*\* \$(.*)", output).group(1).replace(',', ''))
    return data

def parse_flood_data(output):
    """Parses the output of the FloodPolicyAgent."""
    data = {}
    data['flood_availability'] = re.search(r"Insurance Availability:\s*(.*)", output).group(1)
    data['flood_premium'] = float(re.search(r"Estimated Annual Premium:\s*\$(.*)", output).group(1).replace(',', ''))
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

def main():
    """Main function to run the Orchestration Agent."""
    parser = argparse.ArgumentParser(description="Orchestration Agent")
    parser.add_argument("--street", type=str, required=True)
    parser.add_argument("--zip_code", type=str, required=True)
    parser.add_argument("--state", type=str, required=True)
    parser.add_argument("--coverage_type", type=str, required=True)
    parser.add_argument("--project_id", type=str, required=True)
    args = parser.parse_args()

    print("Running PropertyIntelligenceAgent...")
    property_output = run_property_intelligence_agent(args.street, args.zip_code, args.project_id)
    property_data = parse_property_data(property_output)
    
    print("Running FloodPolicyAgent...")
    flood_output = run_flood_policy_agent(args.state, args.coverage_type, args.project_id)
    flood_data = parse_flood_data(flood_output)

    print("Running SAFMRAgent...")
    safmr_output = run_safmr_agent(args.zip_code, args.project_id)
    safmr_data = parse_safmr_data(safmr_output)

    print("Running FinancialLossesAgent...")
    financial_losses_output = run_financial_losses_agent(args.state, args.project_id)
    financial_losses_data = parse_financial_losses_data(financial_losses_output)

    print("Running DealMemoAgent...")
    deal_memo = run_deal_memo_agent(property_data, flood_data, safmr_data, financial_losses_data)

    print("\n--- Generated Deal Memo ---")
    print(deal_memo)

if __name__ == "__main__":
    main()
