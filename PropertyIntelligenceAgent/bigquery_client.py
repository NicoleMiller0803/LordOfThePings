
import os
import subprocess
from google.cloud import bigquery
import pandas as pd

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

def get_property_data(street, zip_code, project_id=None):
    """
    Queries the BigQuery realtor_data dataset for a property.

    Args:
        street (str): The street address of the property.
        zip_code (str): The zip code of the property.
        project_id (str, optional): The Google Cloud Project ID.

    Returns:
        pandas.DataFrame: A DataFrame containing the property data, or None.
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
            *
        FROM
            `RealtorData.realtor_listings`
        WHERE
            street = {float(street)} AND zip_code = {int(zip_code)}
        LIMIT 1
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

def get_comparable_property_data(zip_code, lot_size, building_size, project_id=None):
    """
    Queries the BigQuery realtor_data dataset for comparable properties.

    Args:
        zip_code (str): The zip code of the target property.
        lot_size (float): The lot size of the target property.
        building_size (float): The building size of the target property.
        project_id (str, optional): The Google Cloud Project ID.

    Returns:
        pandas.DataFrame: A DataFrame containing comparable property data, or None.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    if project_id is None:
        project_id = get_gcloud_project()

    if not project_id:
        raise ValueError("Google Cloud Project ID could not be determined. Please set it using 'gcloud config set project' or provide it with the --project_id flag.")

    client = bigquery.Client(project=project_id)

    # Define ranges for comparable properties (+/- 20%)
    lot_size_min = lot_size * 0.8
    lot_size_max = lot_size * 1.2
    building_size_min = building_size * 0.8
    building_size_max = building_size * 1.2
    
    query = f"""
        SELECT
            *
        FROM
            `RealtorData.realtor_listings`
        WHERE
            zip_code = {int(zip_code)}
            AND lot_size BETWEEN {lot_size_min} AND {lot_size_max}
            AND building_size BETWEEN {building_size_min} AND {building_size_max}
            AND listing_status = 'Active'
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
