import boto3
from botocore.exceptions import ClientError

def send_sns_message(topic_arn, message):
    """
    Publishes a message to an SNS topic.
    
    :param topic_arn: ARN of the SNS topic
    :param message: Message to be sent
    :return: The message ID if successful, None otherwise
    """
    sns_client = boto3.client('sns', region_name='ap-south-1')
    
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message
        )
        message_id = response['MessageId']
        print(f"Message published successfully. Message ID: {message_id}")
        return message_id
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Usage example
topic_arn = 'arn:aws:sns:ap-south-1:509399632197:mytopic'
message = 'Hello, this is a test notification from SNS!'

send_sns_message(topic_arn, message)
