import boto3
from datetime import datetime
import uuid
from botocore.exceptions import ClientError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamoDBHelper:
    def __init__(self):
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            self.table = self.dynamodb.Table('ad_copy_requests')
            logger.info("Successfully initialized DynamoDB connection")
            # Test the connection
            self.table.table_status
            logger.info("Successfully connected to table 'ad_copy_requests'")
        except Exception as e:
            logger.error(f"Error initializing DynamoDB: {str(e)}")
            raise

    def store_request(self, request_data, generated_copy):
        """
        Store ad copy request and response in DynamoDB
        """
        try:
            logger.info("Attempting to store request in DynamoDB")
            logger.info(f"Request data: {request_data}")
            
            item = {
                'request_id': str(uuid.uuid4()),
                'timestamp': datetime.utcnow().isoformat(),
                'url': request_data.get('url', ''),
                'product': request_data.get('product', ''),
                'audience': request_data.get('audience', ''),
                'tone': request_data.get('tone', ''),
                'platform': request_data.get('platform', ''),
                'max_length': str(request_data.get('max_length', '')),  # Convert to string
                'generated_copy': generated_copy,
                'status': 'success'
            }
            
            logger.info(f"Prepared item for DynamoDB: {item}")
            
            response = self.table.put_item(Item=item)
            logger.info(f"Successfully stored item in DynamoDB. Response: {response}")
            
            return item['request_id']
        
        except ClientError as e:
            logger.error(f"ClientError storing request in DynamoDB: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error storing request in DynamoDB: {str(e)}")
            return None

    def store_error(self, request_data, error_message):
        """
        Store failed requests in DynamoDB
        """
        try:
            logger.info("Attempting to store error in DynamoDB")
            
            item = {
                'request_id': str(uuid.uuid4()),
                'timestamp': datetime.utcnow().isoformat(),
                'url': request_data.get('url', ''),
                'product': request_data.get('product', ''),
                'error_message': str(error_message),
                'status': 'error'
            }
            
            logger.info(f"Prepared error item for DynamoDB: {item}")
            
            response = self.table.put_item(Item=item)
            logger.info(f"Successfully stored error in DynamoDB. Response: {response}")
            
            return item['request_id']
        
        except ClientError as e:
            logger.error(f"ClientError storing error in DynamoDB: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error storing error in DynamoDB: {str(e)}")
            return None

    def get_request(self, request_id):
        """
        Retrieve a specific request from DynamoDB
        """
        try:
            logger.info(f"Attempting to retrieve request {request_id} from DynamoDB")
            
            response = self.table.get_item(Key={'request_id': request_id})
            logger.info(f"Retrieved response from DynamoDB: {response}")
            
            return response.get('Item')
        except ClientError as e:
            logger.error(f"ClientError retrieving request from DynamoDB: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving request from DynamoDB: {str(e)}")
            return None
