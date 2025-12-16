import os
from google.adk.agents import LlmAgent
from .tools import list_tables, get_table_data

# DEBUG print to check environment variables
print(f"DEBUG: Project={os.getenv('GOOGLE_CLOUD_PROJECT')}, Location={os.getenv('GOOGLE_CLOUD_LOCATION')}")

root_agent = LlmAgent(
    name="bigquery_agent",
    model="gemini-2.5-flash",
    instruction="""You are a BigQuery assistant.
Your goal is to help users explore their BigQuery datasets.
When a user asks about tables in the 'test1' dataset, you should use the 'list_tables' tool with the dataset_id 'test1'.
When asked to summarize a table, use the `get_table_data` tool to get a sample of the data, and then summarize the content of that data. Always specify the dataset_id as 'test1'.
""",
    tools=[list_tables, get_table_data],
)
