from google.cloud import bigquery

def list_tables(dataset_id: str) -> dict:
    """Lists the tables in a given BigQuery dataset.

    Args:
        dataset_id: The ID of the dataset to list tables from.

    Returns:
        A dictionary containing the list of table IDs.
    """
    try:
        client = bigquery.Client()
        tables = client.list_tables(dataset_id)
        table_ids = [table.table_id for table in tables]
        return {"status": "success", "tables": table_ids}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_table_data(dataset_id: str, table_id: str) -> dict:
    """Fetches all rows of a table.

    Args:
        dataset_id: The ID of the dataset.
        table_id: The ID of the table.

    Returns:
        A dictionary containing the table data.
    """
    try:
        client = bigquery.Client()
        table_ref = client.dataset(dataset_id).table(table_id)
        rows = client.list_rows(table_ref)
        data = [dict(row) for row in rows]
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
