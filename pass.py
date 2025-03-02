import boto3

def get_ssm_parameter(parameter_name, with_decryption=True):
    # Create an SSM client
    ssm = boto3.client('ssm', region_name="ap-south-1")  # Change region if needed

    try:
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=with_decryption  # Decrypt if SecureString
        )
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error fetching parameter {parameter_name}: {str(e)}")
        return None

# Fetch parameters
user = get_ssm_parameter("/app/user", with_decryption=False)  # No decryption needed
password = get_ssm_parameter("/app/password", with_decryption=True)  # SecureString needs decryption

if user and password:
    print(f"User: {user}")
    print(f"Password: {password}")  # Be careful printing sensitive data
else:
    print("Failed to fetch parameters.")

