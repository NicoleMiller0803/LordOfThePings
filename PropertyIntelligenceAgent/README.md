
# Property Intelligence Agent

This agent retrieves property information from a BigQuery dataset and generates a structured overview suitable for a commercial loan deal memo.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Google Cloud Project:**
   Make sure your Google Cloud project is set in your environment variables.
   ```bash
   export GOOGLE_CLOUD_PROJECT="ccibt-hack25ww7-738"
   ```

## Usage

Run the agent from the command line with the street and zip code of the property you want to analyze.

```bash
python main.py --street "1265166.0" --zip_code "79758"
```
