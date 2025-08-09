import logging
import os
import azure.functions as func
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool
from dotenv import load_dotenv

load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="query")
def query(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        name = req.params.get('name')
        #req_body = req.get_json()

        # Create an AIProjectClient instance
        project_client = AIProjectClient(
            endpoint=os.environ['PROJECT_ENDPOINT'],  # Use your custom endpoint from .env
            credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
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