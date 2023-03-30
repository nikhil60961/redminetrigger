import logging
import azure.functions as func
import requests
import json
import base64
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Access parameters from environment variables
    organization = os.environ['ORGANIZATION']
    project = os.environ['PROJECT']
    pipeline_id = os.environ['PIPELINE_ID']
    pat_token = os.environ['PAT_TOKEN']
    build_definition_id = os.environ['BUILD_DEFINITION_ID']

    # Set the Azure DevOps REST API endpoint URL for triggering a build
    endpoint_url = f'https://dev.azure.com/{organization}/{project}/_apis/build/builds?api-version=6.1'

    pat_token_b64 = base64.b64encode(bytes(f':{pat_token}', 'ascii')).decode('ascii')
    # Set the headers for the HTTP POST request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat_token_b64}'
    }

    # Set the data for the HTTP POST request
    data = {
        'definition': {'id': build_definition_id}
    }

    # Send the HTTP POST request to trigger the build pipeline
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))

    # Check the response status code and return the result
    if response.status_code == 200:
        # Serialize the response JSON data to a string
        response_json = json.dumps(response.json())
        return func.HttpResponse(body=response_json, status_code=200)
    else:
        return func.HttpResponse(f'Failed to trigger build pipeline. Error: {response.text}')
