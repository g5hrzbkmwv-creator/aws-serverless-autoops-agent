import json
import os
import boto3

sfn = boto3.client('stepfunctions', region_name=os.getenv("AWS_REGION", "ap-southeast-2"))

def lambda_handler(event, context):
    params = event.get('queryStringParameters', {})
    token = params.get('token')
    action = params.get('action')
    sku = params.get('sku')
    qty = int(params.get('qty', 100))

    if not token or not action:
        return {'statusCode': 400, 'body': 'Missing token or action'}

    try:
        if action == 'approve':
            sfn.send_task_success(
                taskToken=token,
                output=json.dumps({'sku': sku, 'quantity': qty})
            )
            return {'statusCode': 200, 'body': f'<h1>✅ Restock Approved for {sku}!</h1>'}
        elif action == 'reject':
            sfn.send_task_failure(
                taskToken=token,
                error='UserRejected',
                cause='Operator rejected via email link.'
            )
            return {'statusCode': 200, 'body': f'<h1>❌ Restock Rejected for {sku}.</h1>'}
        else:
            return {'statusCode': 400, 'body': 'Invalid action'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}