from datetime import datetime, timezone
import logging
import os
import azure.functions as func
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool

from security import MyTokenCredential
import datetime
import re

# Initialize the Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="query")
def query(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    isLocal = os.environ.get("IS_RUNNING_LOCALLY") == "true"
    logging.info(f"Running locally: {isLocal}")

    try:
        name = req.params.get('name')
        # req_body = req.get_json()
        req_headers = req.headers
        access_token = req_headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN")
        expires_on_str = req_headers.get("X-MS-TOKEN-AAD-EXPIRES-ON")
        logging.info(f"Access token: {access_token}")
        logging.info(f"Expires on: {expires_on_str}")

        # Trim microseconds to 6 digits if necessary
        if expires_on_str:
            expires_on_str = re.sub(r'(\.\d{6})\d*Z$', r'\1Z', expires_on_str)
            expires_on = int(datetime.datetime.strptime(expires_on_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                tzinfo=datetime.timezone.utc).timestamp())
        else:
            expires_on = 0
        #Token info can be used to create MyTokenCredential which is TokenCredential but not eligible for ai endpoints
        # MyTokenCredential(
        #    access_token=access_token,
        #    expires_on=expires_on
        # )
        # For AI endpoints we have to use managed identity e.g. system assigned managed identity

        credential = DefaultAzureCredential() # Use Azure Default Credential for authentication, should use managed identity

        # Create an AIProjectClient instance
        project_client = AIProjectClient(
            # Use your custom endpoint from .env
            endpoint=os.environ['PROJECT_ENDPOINT'],
            credential=credential,  # Use Azure Default Credential for authentication
        )

        with project_client:
            # Create an agent with the Bing Grounding tool
            agent = project_client.agents.get_agent(os.environ['AGENT_ID'])

            return func.HttpResponse(
                f"Used agent, ID: {agent.id} with instructions: {agent.instructions}",
                status_code=200
            )

        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(
            f"Error processing request: {e}",
            status_code=500
        )
