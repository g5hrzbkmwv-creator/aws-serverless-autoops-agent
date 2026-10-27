import json
def lambda_handler(event, context):
    sku = event.get('sku', 'UNKNOWN')
    print(f"Restock request for SKU {sku} was REJECTED by human operator.")
    return {'status': 'RESTOCK_REJECTED', 'sku': sku}