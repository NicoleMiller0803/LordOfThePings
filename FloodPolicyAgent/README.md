
# Flood Policy Agent

This agent analyzes flood policy data from a BigQuery dataset to determine insurance availability and estimate annual premiums.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Google Cloud Project (if needed):**
   The agent will try to automatically determine your Google Cloud project ID. If this fails, you can set it as an environment variable:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   ```
   Or, you can provide it as a command-line argument.

## Usage

Run the agent from the command line with the state and coverage type of the property you want to analyze.

```bash
python main.py --state "CALIFORNIA" --coverage_type "Building & Contents" --project_id "ccibt-hack25ww7-738"
```
