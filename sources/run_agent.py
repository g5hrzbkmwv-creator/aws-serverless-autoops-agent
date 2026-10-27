"""
Agent script to test the Gateway
Run this after setup: python run_agent.py
"""

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
# from mcp.client.streamable_http import streamablehttp_client
from mcp.client.streamable_http import streamable_http_client
import httpx
import json
import os
import sys

def create_streamable_http_transport(mcp_url: str):
    # Set GATEWAY_BEARER_TOKEN only for a CUSTOM_JWT gateway
    token = os.environ.get("GATEWAY_BEARER_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else None
    # return streamable_http_client(mcp_url, headers=headers)

    http_client = httpx.AsyncClient(
        headers = {"Authorization": f"Bearer {token}"} if token else None,
        timeout=httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=2.0),
    )

    return streamable_http_client(
        mcp_url,
        http_client=http_client,
    )

def get_full_tools_list(client):
    """Get all tools with pagination support"""
    more_tools = True
    tools = []
    pagination_token = None
    while more_tools:
        tmp_tools = client.list_tools_sync(pagination_token=pagination_token)
        tools.extend(tmp_tools)
        if tmp_tools.pagination_token is None:
            more_tools = False
        else:
            more_tools = True
            pagination_token = tmp_tools.pagination_token
    return tools

def lambda_handler(event, context):

    """
    AWS Lambda Handler: 接收來自 API Gateway 的 Event
    """
    try:

        # Get JSON body from API Gateway event
        body = json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event.get("body", {})
        user_input = body.get("message", "")

        if not user_input:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" # CORS
                },
                "body": json.dumps({"error": "Message is required"})
            }

        # Build the gateway URL from the gateway ID in agentcore status --json
        gateway_url = os.environ.get(
            "GATEWAY_URL"
        )

        # Model configuration - change if needed
        model_id = os.environ.get("MODEL_ID", "amazon.nova-pro-v1:0")

        # Setup Bedrock model
        bedrockmodel = BedrockModel(
            model_id=model_id,
            streaming=True,
        )

        # Setup MCP client
        mcp_client = MCPClient(lambda: create_streamable_http_transport(gateway_url))

        with mcp_client:
            # List available tools
            tools = get_full_tools_list(mcp_client)

            # Create agent
            agent = Agent(model=bedrockmodel, tools=tools)
            response = agent(user_input)

            if isinstance(response, dict):
                output_text = response.get("message", {}).get("content", str(response))
            elif hasattr(response, "message"):
                output_text = response.message.get("content", str(response))
            else:
                output_text = str(response)

        # 4. 回傳給 API Gateway 認得的格式
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"response": output_text})
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }