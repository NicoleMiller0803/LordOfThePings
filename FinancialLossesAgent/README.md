# Financial Losses Agent

This agent connects to BigQuery to analyze financial loss data from the `financial_losses_by_state` table. It provides state-level loss trends.

## Usage

Run the agent from the command line, providing the required state.

```bash
python main.py \
    --state "CALIFORNIA" \
    --project_id "ccibt-hack25ww7-738"
```

