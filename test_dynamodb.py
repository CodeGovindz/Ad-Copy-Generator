import boto3
from botocore.exceptions import ClientError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_dynamodb_connection():
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        logger.info("Successfully created DynamoDB resource")
        
        # List all tables
        table_list = list(dynamodb.tables.all())
        logger.info(f"Found tables: {[table.name for table in table_list]}")
        
        # Try to get the specific table
        table = dynamodb.Table('ad_copy_requests')
        table.table_status  # This will fail if table doesn't exist
        logger.info("Successfully connected to ad_copy_requests table")
        
        # Try to write a test item
        test_item = {
            'request_id': 'test-item',
            'test_field': 'test_value'
        }
        response = table.put_item(Item=test_item)
        logger.info(f"Successfully wrote test item. Response: {response}")
        
        # Try to read the test item
        response = table.get_item(Key={'request_id': 'test-item'})
        logger.info(f"Successfully read test item: {response.get('Item')}")
        
        # Clean up test item
        table.delete_item(Key={'request_id': 'test-item'})
        logger.info("Successfully deleted test item")
        
        return True
        
    except ClientError as e:
        logger.error(f"AWS error occurred: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing DynamoDB connection...")
    success = test_dynamodb_connection()
    print(f"Test {'succeeded' if success else 'failed'}")
