import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    sku = event.get('sku', 'ITEM-001')
    response = table.get_item(Key={'SKU': sku})
    item = response.get('Item', {'SKU': sku, 'quantity': 10, 'safe_level': 50})
    
    quantity = int(item.get('quantity', 0))
    safe_level = int(item.get('safe_level', 50))
    
    return {
        'sku': sku,
        'current_quantity': quantity,
        'safe_level': safe_level,
        'needs_restock': quantity < safe_level
    }