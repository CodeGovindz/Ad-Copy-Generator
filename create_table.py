import boto3
from botocore.exceptions import ClientError

def create_dynamodb_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        table = dynamodb.create_table(
            TableName='ad_copy_requests',
            KeySchema=[
                {
                    'AttributeName': 'request_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'request_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for the table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName='ad_copy_requests')
        print("Table created successfully!")
        return True
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists!")
            return True
        else:
            print(f"Error creating table: {str(e)}")
            return False

if __name__ == "__main__":
    create_dynamodb_table()
