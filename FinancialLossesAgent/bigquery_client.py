
import os
import subprocess
from google.cloud import bigquery

def get_gcloud_project():
    """Gets the default gcloud project."""
    try:
        project = subprocess.check_output(
            ["gcloud", "config", "get-value", "project"],
            stderr=subprocess.PIPE,
            text=True
        ).strip()
        return project
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_financial_loss_data(state, project_id=None):
    """
    Queries the BigQuery financial_losses_by_state table for a state.

    Args:
        state (str): The state to filter by.
        project_id (str, optional): The Google Cloud Project ID.

    Returns:
        pandas.DataFrame: A DataFrame containing the financial loss data, or None.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    if project_id is None:
        project_id = get_gcloud_project()

    if not project_id:
        raise ValueError("Google Cloud Project ID could not be determined. Please set it using 'gcloud config set project' or provide it with the --project_id flag.")

    client = bigquery.Client(project=project_id)
    
    query = f"""
        SELECT
            `State`,
            ` Number of Records `,
            ` Closed With Payment Losses `,
            ` Open Losses `,
            ` Closed Without Payment Losses `,
            ` Total Payments `
        FROM
            `test1.financial_losses_by_state`
        WHERE
            State = '{state.upper()}'
    """

    try:
        query_job = client.query(query)
        results = query_job.to_dataframe()
        if not results.empty:
            return results
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
