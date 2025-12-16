
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

def get_safmr_data(zip_code, project_id=None):
    """
    Queries the BigQuery SAFMR datasets for a property.

    Args:
        zip_code (str): The zip code of the property.
        project_id (str, optional): The Google Cloud Project ID.

    Returns:
        pandas.DataFrame: A DataFrame containing the SAFMR data, or None.
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
            zipcode,
            hud_area_code,
            hud_fair_market_rent_area_name,
            safmr0br,
            safmr0br_90paymentstandard,
            safmr0br_110paymentstandard,
            safmr1br,
            safmr1br_90paymentstandard,
            safmr1br_110paymentstandard,
            safmr2br,
            safmr2br_90paymentstandard,
            safmr2br_110paymentstandard,
            safmr3br,
            safmr3br_90paymentstandard,
            safmr3br_110paymentstandard,
            safmr4br,
            safmr4br_90paymentstandard,
            safmr4br_110paymentstandard,
            program_name,
            year
        FROM
            (
                SELECT
                    zipcode,
                    hud_area_code,
                    hud_fair_market_rent_area_name,
                    safmr0br,
                    safmr0br_90paymentstandard,
                    safmr0br_110paymentstandard,
                    safmr1br,
                    safmr1br_90paymentstandard,
                    safmr1br_110paymentstandard,
                    safmr2br,
                    safmr2br_90paymentstandard,
                    safmr2br_110paymentstandard,
                    safmr3br,
                    safmr3br_90paymentstandard,
                    safmr3br_110paymentstandard,
                    safmr4br,
                    safmr4br_90paymentstandard,
                    safmr4br_110paymentstandard,
                    'safmr_2026' as program_name,
                    2026 as year,
                    ROW_NUMBER() OVER(PARTITION BY zipcode ORDER BY 2026 DESC) as rn
                FROM
                    `test1.safmr_2026`
                WHERE
                    zipcode = {int(zip_code)}
                UNION ALL
                SELECT
                    zipcode,
                    hud_area_code,
                    hud_fair_market_rent_area_name,
                    safmr0br,
                    safmr0br_90paymentstandard,
                    safmr0br_110paymentstandard,
                    safmr1br,
                    safmr1br_90paymentstandard,
                    safmr1br_110paymentstandard,
                    safmr2br,
                    safmr2br_90paymentstandard,
                    safmr2br_110paymentstandard,
                    safmr3br,
                    safmr3br_90paymentstandard,
                    safmr3br_110paymentstandard,
                    safmr4br,
                    safmr4br_90paymentstandard,
                    safmr4br_110paymentstandard,
                    'safmrs_2025' as program_name,
                    2025 as year,
                    ROW_NUMBER() OVER(PARTITION BY zipcode ORDER BY 2025 DESC) as rn
                FROM
                    `test1.safmrs_2025`
                WHERE
                    zipcode = {int(zip_code)}
            )
        WHERE
            rn = 1
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
