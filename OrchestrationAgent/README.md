# Orchestration Agent

This agent orchestrates the execution of the `PropertyIntelligenceAgent`, `FloodPolicyAgent`, and `DealMemoAgent` to generate a final deal memo from basic property identifiers.

## Usage

Run the agent from the command line, providing the required property identifiers.

```bash
python main.py \
    --street "1265166.0" \
    --zip_code "79758" \
    --state "CALIFORNIA" \
    --coverage_type "Building & Contents" \
    --project_id "ccibt-hack25ww7-738"
```

