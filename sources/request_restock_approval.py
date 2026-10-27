import json
import os
import boto3

sfn = boto3.client('stepfunctions', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))

def lambda_handler(event, context):
    sku = event.get('sku')
    quantity = event.get('quantity', 100)
    
    # 啟動 Step Functions (這會建立 taskToken 並等待)
    response = sfn.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],
        input=json.dumps({'sku': sku, 'quantity': quantity})
    )
    return {
        'status': 'APPROVAL_PENDING',
        'message': f'Restock approval workflow initiated for SKU: {sku}. Check your email.',
        'executionArn': response['executionArn']
    }