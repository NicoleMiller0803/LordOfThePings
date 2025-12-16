# SAFMR Agent

This agent connects to BigQuery to analyze Small Area Fair Market Rents (SAFMR) data from the `safmr_2026` and `safmrs_2025` tables. It provides a market pricing analysis for a given property.

## Usage

Run the agent from the command line, providing the required property identifiers.

```bash
python main.py \
    --zip_code "79758" \
    --project_id "ccibt-hack25ww7-738"
```

