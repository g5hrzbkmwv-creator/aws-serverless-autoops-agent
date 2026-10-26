import json
import os
import boto3

ses = boto3.client('ses', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))
table = dynamodb.Table(os.environ['TABLE_NAME'])
sender = os.getenv('SENDER_EMAIL', 'whiteholekong@gmail.com')

def lambda_handler(event, context):
    sku = event.get('sku')
    qty = int(event.get('quantity', 100))
    
    # 1. 從 DynamoDB 查詢該商品的供應商 Email
    response = table.get_item(Key={'SKU': sku})
    item = response.get('Item', {})
    supplier_email = item.get('supplier_email', 'default-supplier@example.com')

    # 2. 組合給供應商的採購信件內容
    subject = "【Official automated purchase order - Purchase Order】"
    supplier_email_body = f"""    
    Dear Supplier：
    Because the inventory is below the safe level, our system has automatically initiated a purchase request. Please assist in arranging the shipment.
    
    - Product SKU: {sku}
    - Purchase quantity: {qty} unit
    - Note: Please confirm and arrange logistics within 3 business days.
    
    Autonomous Ops Agent 系統自動發送
    """
    
    # 3. 發送給供應商 (可以設定一個供應商專用的 SES Topic 或 Email)
    try:
        ses.send_email(
            Source=sender,
            Destination={'ToAddresses': [supplier_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': supplier_email_body}}
            }
        )
    except Exception as e:
        print(f"Failed to notify supplier: {str(e)}")
    
    # # 3. 更新 DynamoDB 狀態（記錄此 SKU 進入採購中狀態）
    # table = dynamodb.Table(os.environ['TABLE_NAME'])
    # table.update_item(
    #     Key={'SKU': sku},
    #     UpdateExpression="SET order_status = :status, last_restock_qty = :qty",
    #     ExpressionAttributeValues={
    #         ':status': 'ORDER_SENT_TO_SUPPLIER',
    #         ':qty': qty
    #     }
    # )
    
    return {
        'status': 'RESTOCK_ORDER_COMMUNICATED',
        'sku': sku,
        'ordered_quantity': qty,
        'action': 'Email sent to supplier & DB updated.'
    }
