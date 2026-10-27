import json
import os
import boto3
import urllib.parse

sns = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))

def lambda_handler(event, context):
    sku = event.get('sku')
    quantity = event.get('quantity')
    task_token = event.get('taskToken')

    # 產生帶有 taskToken 的同意/拒絕連結
    api_url = os.environ['API_ENDPOINT']
    token_encoded = urllib.parse.quote(task_token)
    
    approve_link = f"{api_url}?token={token_encoded}&action=approve&sku={sku}&qty={quantity}"
    reject_link = f"{api_url}?token={token_encoded}&action=reject&sku={sku}"

    message = f"""
    [AI Agent Approval Notice]
    The system detected insufficient inventory and intends to replenish the stock.
    
    Product SKU: {sku}
    Quantity: {quantity}
    
    Please click the following link to proceed with the approval:
    ✅ Approve: {approve_link}
    ❌ Reject: {reject_link}
    """

    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject=f"⚠️ Approval Requirements: Product {sku} Restocking",
        Message=message
    )
    return {"status": "EMAIL_SENT"}
