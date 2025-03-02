import boto3
import json
from datetime import datetime

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')  # e.g., 'us-east-1'

# Specify the DynamoDB table name
table_name = "MyPythonOutputs"

def store_output_in_dynamodb(output):
    try:
        # Connect to the DynamoDB table
        table = dynamodb.Table(table_name)
        
        # Store into the table
        table.put_item(Item=output)

        print(f"Successfully stored the output: {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The data you want to store (modify as needed)
    output = {
        "id": "123",  # Unique identifier for the record
        "result": "Hello from EC2!",
        "timestamp": datetime.utcnow().isoformat()  # Current timestamp in UTC
    }
    
    # Call the function to store output in DynamoDB
    store_output_in_dynamodb(output)
