# BigQuery Agent

This agent connects to a BigQuery dataset to answer user questions.

## Setup

1.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Copy the `.env.example` file to `.env` and fill in your Google Cloud project details.

    ```bash
    cp .env.example .env
    ```

3.  **Authenticate with Google Cloud:**
    ```bash
    gcloud auth application-default login
    ```

## Run

You can run the agent using the ADK CLI:

```bash
adk run .
```

Then, you can ask questions like: "What tables are in the test1 dataset?"
