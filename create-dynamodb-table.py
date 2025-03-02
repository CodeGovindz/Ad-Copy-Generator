import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DynamoDB configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "AdCopyGenerator")

def create_dynamodb_table():
    """
    Create a DynamoDB table for storing ad copy generator data
    """
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    
    # Check if table already exists
    existing_tables = [table.name for table in dynamodb.tables.all()]
    if DYNAMODB_TABLE in existing_tables:
        print(f"Table {DYNAMODB_TABLE} already exists.")
        return
    
    # Create the table
    table = dynamodb.create_table(
        TableName=DYNAMODB_TABLE,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'  # String
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName=DYNAMODB_TABLE)
    print(f"Table {DYNAMODB_TABLE} created successfully.")

if __name__ == "__main__":
    create_dynamodb_table()
