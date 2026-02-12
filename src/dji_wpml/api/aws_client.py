import boto3
from botocore.exceptions import ClientError
import os

class AwsClient:
    """
    Client class for interacting with Amazon S3 using temporary STS credentials 
    obtained from the FlightHub API.
    """
    def __init__(self):
        # Initialize internal state to None
        self._s3_client = None
        self._bucket_name = None
        self._object_key_prefix = None
        self._region = None
        print("AwsClient initialized. Credentials required for use.")

    def setup_credentials(self, api_response_data: dict):
        """
        Sets up the Boto3 client using the temporary credentials and configuration 
        from the FlightHub API response (API 1: Get Temporary Upload Token).
        
        Args:
            api_response_data: The 'data' dictionary from the API response body.
        """
        credentials = api_response_data.get('credentials', {})
        
        access_key_id = credentials.get('access_key_id')
        access_key_secret = credentials.get('access_key_secret')
        security_token = credentials.get('security_token')
        
        self._bucket_name = api_response_data.get('bucket')

        self._object_key_prefix = api_response_data.get('object_key_prefix')

        # S3 uses 'region' for endpoint specification
        self._region = api_response_data.get('region') 

        if not all([access_key_id, access_key_secret, security_token, self._bucket_name, self._object_key_prefix, self._region]):
            raise ValueError("Missing essential credentials or configuration from API response.")
        
        print("Setting up Boto3 S3 client with temporary credentials...")
        print(f"Bucket: {self._bucket_name}, Prefix: {self._object_key_prefix}, Region: {self._region}")

        # 1. Create the Boto3 Session using temporary STS credentials
        try:
            session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key_secret,
                aws_session_token=security_token,
                region_name=self._region
            )
            
            # 2. Create the S3 Client object for upload operations
            self._s3_client = session.client('s3')
            
            print("Boto3 S3 client successfully set and ready for use.")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Boto3 session or client: {e}")

    def put_object(self, local_file_path: str, file_name: str) -> str:
        """
        Uploads a local file to the designated S3 bucket location using the 
        pre-configured project key prefix.

        Args:
            local_file_path: Absolute path to the file on the local file system.
            file_name: The desired name of the file in the bucket (e.g., 'route.kmz').
            
        Returns:
            The final object_key (full path) in the bucket on success, or raises an error.
        """
        if self._s3_client is None:
            raise RuntimeError("Client not configured. Call setup_credentials() first.")

        # Construct the final S3 object key: prefix + filename
        # S3 keys always use forward slashes
        final_object_key = os.path.join(self._object_key_prefix, file_name).replace('\\', '/')
        
        print(f"Attempting upload to S3 key: s3://{self._bucket_name}/{final_object_key}")

        try:
            # Boto3 method for uploading a file
            self._s3_client.upload_file(
                Filename=local_file_path,
                Bucket=self._bucket_name,
                Key=final_object_key,
                # Optional: Add ACL/Metadata if required by your system
                # ExtraArgs={'ContentType': 'application/vnd.google-earth.kmz'} 
            )
            
            print(f"✅ Upload successful. File stored at: {final_object_key}")
            return final_object_key
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Local file not found at: {local_file_path}")
        except ClientError as e:
            # Catch specific Boto3/S3 errors (e.g., permission denied, bucket not found)
            raise IOError(f"AWS S3 client error during upload: {e}")
        